import os
import unittest
import numpy as np
from pyNastran.dev.solver.solver import Solver, BDF
from pyNastran.bdf.case_control_deck import CaseControlDeck


class TestSpring(unittest.TestCase):
    def test_celas1(self):
        """Tests a CELAS1/PELAS"""
        model = BDF(debug=True, log=None, mode='msc')
        model.bdf_filename = 'celas1.bdf'
        model.add_grid(1, [0., 0., 0.])
        model.add_grid(2, [0., 0., 0.])
        nids = [1, 2]
        eid = 1
        pid = 2
        model.add_celas1(eid, pid, nids, c1=1, c2=1, comment='')
        k = 1000.

        load_id = 2
        spc_id = 3
        model.add_pelas(pid, k, ge=0., s=0., comment='')
        # model.add_sload(load_id, 2, 20.)
        fxyz = [1., 0., 0.]
        mag = 20.
        model.add_force(load_id, 2, mag, fxyz, cid=0, comment='')

        components = 123456
        nodes = 1
        model.add_spc1(spc_id, components, nodes, comment='')
        setup_case_control(model)

        solver = Solver(model)
        model.sol = 103
        solver.run()

        model.sol = 101
        solver.run()

        # F = k * d
        # d = F / k
        # 20=1000.*d
        d = mag / k
        assert np.allclose(solver.xa_[0], d)
        os.remove(solver.f06_filename)
        os.remove(solver.op2_filename)

    def test_celas2_cd(self):
        """Tests a CELAS2"""
        model = BDF(debug=True, log=None, mode='msc')
        model.bdf_filename = 'celas2.bdf'
        model.add_grid(1, [0., 0., 0.])
        cd = 100
        model.add_grid(2, [0., 0., 0.], cd=cd)
        origin = [0., 0., 0.]
        zaxis = [0., 0., 1.]
        xzplane = [0., 1., 0.]
        model.add_cord2r(cd, origin, zaxis, xzplane, rid=0, setup=True, comment='')
        nids = [1, 2]
        eid = 1
        k = 1000.
        model.add_celas2(eid, k, nids, c1=1, c2=2, ge=0., s=0., comment='')

        load_id = 2
        spc_id = 3
        # model.add_sload(load_id, 2, 20.)
        fxyz = [1., 0., 0.]
        mag = 20.
        model.add_force(load_id, 2, mag, fxyz, cid=0, comment='')

        components = 123456
        nodes = 1
        model.add_spc1(spc_id, components, nodes, comment='')
        setup_case_control(model)

        solver = Solver(model)
        solver.run()

        # F = k * d
        d = mag / k
        assert np.allclose(solver.xa_[0], d)


class TestRod(unittest.TestCase):
    """tests the rods"""
    def test_crod_axial(self):
        """Tests a CROD/PROD"""
        model = BDF(debug=True, log=None, mode='msc')
        model.bdf_filename = 'crod_axial.bdf'
        model.add_grid(1, [0., 0., 0.])
        model.add_grid(2, [1., 0., 0.])
        nids = [1, 2]
        eid = 1
        pid = 2
        mid = 3
        E = 3.0e7
        G = None
        nu = 0.3
        model.add_mat1(mid, E, G, nu, rho=0.0, a=0.0, tref=0.0, ge=0.0, St=0.0,
                       Sc=0.0, Ss=0.0, mcsid=0)
        model.add_crod(eid, pid, nids)
        model.add_prod(pid, mid, A=1.0, j=0., c=0., nsm=0.)

        load_id = 2
        spc_id = 3
        nid = 2
        mag = 1.
        fxyz = [1., 0., 0.]
        model.add_force(load_id, nid, mag, fxyz, cid=0)

        components = 123456
        nodes = 1
        model.add_spc1(spc_id, components, nodes, comment='')
        setup_case_control(model)
        solver = Solver(model)
        #with self.assertRaises(RuntimeError):
        solver.run()

    def test_crod_torsion(self):
        """Tests a CROD/PROD"""
        model = BDF(debug=True, log=None, mode='msc')
        model.bdf_filename = 'crod_torsion.bdf'
        model.add_grid(1, [0., 0., 0.])
        model.add_grid(2, [1., 0., 0.])
        nids = [1, 2]
        eid = 1
        pid = 2
        mid = 3
        E = 3.0e7
        G = None
        nu = 0.3
        model.add_mat1(mid, E, G, nu, rho=0.0, a=0.0, tref=0.0, ge=0.0, St=0.0,
                       Sc=0.0, Ss=0.0, mcsid=0)
        model.add_crod(eid, pid, nids)
        model.add_prod(pid, mid, A=0.0, j=2., c=0., nsm=0.)

        load_id = 2
        spc_id = 3
        nid = 2
        mag = 1.
        fxyz = [1., 0., 0.]
        model.add_moment(load_id, nid, mag, fxyz, cid=0)

        components = 123456
        nodes = 1
        model.add_spc1(spc_id, components, nodes, comment='')
        setup_case_control(model)
        solver = Solver(model)
        solver.run()

    def test_crod_spcd(self):
        """Tests a CROD/PROD with an SPCD and no free DOFs"""
        model = BDF(debug=True, log=None, mode='msc')
        model.bdf_filename = 'crod_spcd.bdf'
        model.add_grid(1, [0., 0., 0.])
        model.add_grid(2, [1., 0., 0.])
        nids = [1, 2]
        eid = 1
        pid = 2
        mid = 3
        E = 42.
        G = None
        nu = 0.3
        model.add_mat1(mid, E, G, nu, rho=0.0, a=0.0, tref=0.0, ge=0.0, St=0.0,
                       Sc=0.0, Ss=0.0, mcsid=0)
        model.add_crod(eid, pid, nids)
        model.add_prod(pid, mid, A=1.0, j=0., c=0., nsm=0.)

        load_id = 2
        spc_id = 3
        nid = 2
        mag = 1.
        fxyz = [0., 0., 0.]
        model.add_force(load_id, nid, mag, fxyz, cid=0)

        nodes = 1
        components = 123456
        #model.add_spc1(spc_id, components, nodes, comment='')
        model.add_spc(spc_id, nodes, components, 0., comment='')

        #components = 123456
        #nodes = 1
        #enforced = 0.1
        #model.add_spc(spc_id, nodes, components, enforced, comment='')
        nodes = 2
        components = 1
        enforced = 0.1
        model.add_spcd(load_id, nodes, components, enforced, comment='')

        components = '1'
        model.add_spcd(9999999, nodes, components, enforced, comment='')

        components = 123456
        #model.add_spc1(spc_id, components, nodes, comment='')
        model.add_spc(spc_id, nodes, components, 0., comment='')
        setup_case_control(model)
        solver = Solver(model)
        solver.run()
        # F = kx
        dx = enforced
        k = E
        F = k * dx
        assert len(solver.xa_) == 0, solver.xa_
        assert len(solver.Fa_) == 0, solver.Fa_
        assert np.allclose(solver.xg[6], dx), solver.xa_
        assert np.allclose(solver.Fg[6], F), solver.xa_
        #assert np.allclose(solver.Fa_[0], 0.), solver.Fa_


    def test_crod(self):
        """Tests a CROD/PROD"""
        model = BDF(debug=True, log=None, mode='msc')
        model.bdf_filename = 'crod.bdf'
        model.add_grid(1, [0., 0., 0.])
        model.add_grid(2, [1., 0., 0.])
        nids = [1, 2]
        eid = 1
        pid = 2
        mid = 3
        E = 3.0e7
        G = None
        nu = 0.3
        model.add_mat1(mid, E, G, nu, rho=0.0, a=0.0, tref=0.0, ge=0.0, St=0.0,
                       Sc=0.0, Ss=0.0, mcsid=0)
        model.add_crod(eid, pid, nids)
        model.add_prod(pid, mid, A=1.0, j=2., c=0., nsm=0.)

        load_id = 2
        spc_id = 3
        nid = 2
        mag = 1.
        fxyz = [1., 0., 0.]
        model.add_force(load_id, nid, mag, fxyz, cid=0)

        components = 123456
        nodes = 1
        model.add_spc1(spc_id, components, nodes, comment='')
        setup_case_control(model)
        solver = Solver(model)
        solver.run()

    def test_crod_aset(self):
        """
        Tests a CROD/PROD using an ASET

        same answer as ``test_crod``
        """
        model = BDF(debug=True, log=None, mode='msc')
        model.bdf_filename = 'crod_aset.bdf'
        model.add_grid(1, [0., 0., 0.])
        model.add_grid(2, [1., 0., 0.])
        nids = [1, 2]
        eid = 1
        pid = 2
        mid = 3
        E = 3.0e7
        G = None
        nu = 0.3
        model.add_mat1(mid, E, G, nu, rho=0.0, a=0.0, tref=0.0, ge=0.0, St=0.0,
                       Sc=0.0, Ss=0.0, mcsid=0)
        model.add_crod(eid, pid, nids)
        model.add_prod(pid, mid, A=1.0, j=2., c=0., nsm=0.)

        load_id = 2
        spc_id = 3
        nid = 2
        mag = 1.
        fxyz = [1., 0., 0.]
        model.add_force(load_id, nid, mag, fxyz, cid=0)

        components = 123456
        nodes = 1
        model.add_spc1(spc_id, components, nodes, comment='')

        aset_ids = 2
        aset_components = '456'
        model.add_aset(aset_ids, aset_components)

        aset_ids = [2, 2]
        aset_components = ['456', '123']
        model.add_aset1(aset_ids, aset_components, comment='')

        setup_case_control(model)
        solver = Solver(model)
        solver.run()

    def test_crod_mpc(self):
        """Tests a CROD/PROD"""
        model = BDF(debug=True, log=None, mode='msc')
        model.bdf_filename = 'crod_mpc.bdf'
        model.add_grid(1, [0., 0., 0.])
        model.add_grid(2, [1., 0., 0.])
        model.add_grid(3, [1., 0., 0.])
        nids = [1, 2]
        eid = 1
        pid = 2
        mid = 3
        E = 3.0e7
        G = None
        nu = 0.3
        model.add_mat1(mid, E, G, nu, rho=0.0, a=0.0, tref=0.0, ge=0.0, St=0.0,
                       Sc=0.0, Ss=0.0, mcsid=0)
        model.add_crod(eid, pid, nids)
        model.add_prod(pid, mid, A=1.0, j=2., c=0., nsm=0.)
        mpc_id = 10
        nodes = [2, 3]
        components = [1, 3]
        coefficients = [1., -1.]
        model.add_mpc(mpc_id, nodes, components, coefficients)

        load_id = 2
        spc_id = 3
        nid = 3
        mag = 1.
        fxyz = [0., 0., 1.]
        model.add_force(load_id, nid, mag, fxyz, cid=0)

        components = 123456
        nodes = 1
        model.add_spc1(spc_id, components, nodes, comment='')
        setup_case_control(model, extra_case_lines=['MPC=10'])
        solver = Solver(model)
        solver.run()

    def test_ctube(self):
        """Tests a CTUBE/PTUBE"""
        model = BDF(debug=True, log=None, mode='msc')
        model.bdf_filename = 'ctube.bdf'
        model.add_grid(1, [0., 0., 0.])
        model.add_grid(2, [1., 0., 0.])
        nids = [1, 2]
        eid = 1
        pid = 2
        mid = 3
        E = 3.0e7
        G = None
        nu = 0.3
        model.add_mat1(mid, E, G, nu, rho=0.0, a=0.0, tref=0.0, ge=0.0, St=0.0,
                       Sc=0.0, Ss=0.0, mcsid=0)
        model.add_ctube(eid, pid, nids)
        OD1 = 1.0
        model.add_ptube(pid, mid, OD1, t=0.1, nsm=0., OD2=None, comment='')

        load_id = 2
        spc_id = 3
        nid = 2
        mag = 1.
        fxyz = [1., 0., 0.]
        model.add_force(load_id, nid, mag, fxyz, cid=0)

        components = 123456
        nodes = 1
        model.add_spc1(spc_id, components, nodes, comment='')
        setup_case_control(model)
        solver = Solver(model)
        solver.run()

        # F = k * x
        # x = F / k

    def test_conrod(self):
        """Tests a CONROD"""
        model = BDF(debug=True, log=None, mode='msc')
        model.bdf_filename = 'conrod.bdf'
        L = 1.
        model.add_grid(1, [0., 0., 0.])
        model.add_grid(2, [L, 0., 0.])

        nids = [1, 2]
        eid = 1
        mid = 3
        E = 200.
        G = None
        nu = 0.3
        model.add_mat1(mid, E, G, nu, rho=0.0, a=0.0, tref=0.0, ge=0.0, St=0.0,
                       Sc=0.0, Ss=0.0, mcsid=0)
        A = 1.0
        J = 2.0
        model.add_conrod(eid, mid, nids, A=A, j=J, c=0.0, nsm=0.0)

        load_id = 2
        spc_id = 3
        nid = 2
        mag_axial = 10000.
        fxyz = [1., 0., 0.]
        model.add_force(load_id, nid, mag_axial, fxyz, cid=0)

        mag_torsion = 20000.
        fxyz = [1., 0., 0.]
        model.add_moment(load_id, nid, mag_torsion, fxyz, cid=0)

        components = 123456
        nodes = 1
        model.add_spc1(spc_id, components, nodes, comment='')

        #nodes = 2
        #model.add_spc1(spc_id, 23456, nodes, comment='')
        setup_case_control(model)
        solver = Solver(model)
        solver.run()

        # TODO: why is this a torsional result???
        G = E / (2 * (1 + nu))
        kaxial = A * E / L
        ktorsion = G * J / L
        # F = k * d
        daxial = mag_axial / kaxial
        dtorsion = mag_torsion / ktorsion
        print(solver.xa_)
        assert np.allclose(solver.xa_[0], daxial), f'daxial={daxial} kaxial={kaxial} xa_={solver.xa_}'
        assert np.allclose(solver.xa_[1], dtorsion), f'dtorsion={dtorsion} ktorsion={ktorsion} xa_={solver.xa_}'

class TestBar(unittest.TestCase):
    """tests the CBARs"""
    def test_cbar(self):
        """Tests a CBAR/PBAR"""
        model = BDF(debug=True, log=None, mode='msc')
        model.bdf_filename = 'cbar.bdf'
        model.add_grid(1, [0., 0., 0.])
        model.add_grid(2, [1., 0., 0.])
        nids = [1, 2]
        eid = 1
        pid = 2
        mid = 3
        E = 3.0e7
        G = None
        nu = 0.3
        model.add_mat1(mid, E, G, nu, rho=0.0, a=0.0, tref=0.0, ge=0.0, St=0.0,
                       Sc=0.0, Ss=0.0, mcsid=0)

        x = [0., 1., 0.]
        g0 = None
        model.add_cbar(eid, pid, nids, x, g0,
                       offt='GGG', pa=0, pb=0, wa=None, wb=None, comment='')
        model.add_pbar(pid, mid,
                       A=1., i1=1., i2=1., i12=1., j=1.,
                       nsm=0.,
                       c1=0., c2=0., d1=0., d2=0.,
                       e1=0., e2=0., f1=0., f2=0.,
                       k1=1.e8, k2=1.e8, comment='')
        load_id = 2
        spc_id = 3
        nid = 2
        mag = 1.
        fxyz = [1., 0., 0.]
        model.add_force(load_id, nid, mag, fxyz, cid=0)

        components = 123456
        nodes = 1
        model.add_spc1(spc_id, components, nodes, comment='')
        setup_case_control(model)
        solver = Solver(model)
        solver.run()

    def test_cbeam(self):
        """Tests a CBEAM/PBEAM"""
        model = BDF(debug=True, log=None, mode='msc')
        model.bdf_filename = 'cbeam.bdf'
        model.add_grid(1, [0., 0., 0.])
        model.add_grid(2, [1., 0., 0.])
        nids = [1, 2]
        eid = 1
        pid = 2
        mid = 3
        E = 3.0e7
        G = None
        nu = 0.3
        model.add_mat1(mid, E, G, nu, rho=0.0, a=0.0, tref=0.0, ge=0.0, St=0.0,
                       Sc=0.0, Ss=0.0, mcsid=0)

        x = [0., 1., 0.]
        g0 = None
        model.add_cbeam(eid, pid, nids, x, g0, offt='GGG', bit=None,
                        pa=0, pb=0, wa=None, wb=None, sa=0, sb=0, comment='')
        #beam_type = 'BAR'
        xxb = [0.]
        #dims = [[1., 2.]]
        #model.add_pbeaml(pid, mid, beam_type, xxb, dims,
                         #so=None, nsm=None, group='MSCBML0', comment='')
        so = ['YES']
        area = [1.0]
        i1 = [1.]
        i2 = [2.]
        i12 = [0.]
        j = [2.]
        model.add_pbeam(pid, mid, xxb, so, area, i1, i2, i12, j, nsm=None,
                        c1=None, c2=None, d1=None, d2=None, e1=None, e2=None, f1=None, f2=None,
                        k1=1., k2=1., s1=0., s2=0., nsia=0., nsib=None, cwa=0., cwb=None,
                        m1a=0., m2a=0., m1b=None, m2b=None, n1a=0., n2a=0., n1b=None, n2b=None,
                        comment='')
        load_id = 2
        spc_id = 3
        nid = 2
        mag = 1.
        fxyz = [1., 0., 0.]
        model.add_force(load_id, nid, mag, fxyz, cid=0)

        components = 123456
        nodes = 1
        model.add_spc1(spc_id, components, nodes, comment='')
        setup_case_control(model)
        solver = Solver(model)
        solver.run()

def setup_case_control(model, extra_case_lines=None):
    lines = [
        'STRESS(PLOT,PRINT) = ALL',
        'STRAIN(PLOT,PRINT) = ALL',
        'FORCE(PLOT,PRINT) = ALL',
        'DISP(PLOT,PRINT) = ALL',
        'GPFORCE(PLOT,PRINT) = ALL',
        'SPCFORCE(PLOT,PRINT) = ALL',
        'MPCFORCE(PLOT,PRINT) = ALL',
        'OLOAD(PLOT,PRINT) = ALL',
        'SUBCASE 1',
        '  LOAD = 2',
        '  SPC = 3',
    ]
    if extra_case_lines is not None:
        lines += extra_case_lines
    cc = CaseControlDeck(lines, log=model.log)
    model.sol = 101
    model.case_control_deck = cc

class TestShell(unittest.TestCase):
    """tests the shells"""
    def test_cquad4_bad_normal(self):
        """test that the code crashes with a bad normal"""
        model = BDF(debug=False, log=None, mode='msc')
        model.bdf_filename = 'cquad4_bad_normal.bdf'
        mid = 3
        model.add_grid(1, [0., 0., 0.])
        model.add_grid(3, [1., 0., 0.])
        model.add_grid(2, [1., 0., 2.])
        model.add_grid(4, [0., 0., 2.])
        nids = [1, 2, 3, 4]
        model.add_cquad4(5, 5, nids, theta_mcid=0.0, zoffset=0., tflag=0,
                         T1=None, T2=None, T3=None, T4=None, comment='')
        model.add_pcomp(5, [mid], [0.1], thetas=None,
                        souts=None, nsm=0., sb=0., ft=None, tref=0., ge=0., lam=None, z0=None, comment='')

        E = 1.0E7
        G = None
        nu = 0.3
        model.add_mat1(mid, E, G, nu, rho=0.0, a=0.0, tref=0.0, ge=0.0,
                       St=0.0, Sc=0.0, Ss=0.0, mcsid=0, comment='')
        spc_id = 3
        load_id = 2
        components = '123456'
        nodes = [1, 2]
        model.add_spc1(spc_id, components, nodes, comment='')
        model.add_force(load_id, 3, 1.0, [0., 0., 1.], cid=0, comment='')
        model.add_force(load_id, 4, 1.0, [0., 0., 1.], cid=0, comment='')

        setup_case_control(model)
        solver = Solver(model)

        with self.assertRaises(RuntimeError):
            # invalid normal vector
            solver.run()
        #os.remove(model.bdf_filename)

    def test_cquad4_bad_jacobian(self):
        """
        Tests that the code crashes with a really terrible CQUAD4

        The Jacobian is defined between [-1, 1]
        """
        model = BDF(debug=False, log=None, mode='msc')
        model.bdf_filename = 'cquad4_bad_jacobian.bdf'
        mid = 3
        model.add_grid(1, [0., 0., 0.])
        model.add_grid(2, [0.5, 100., 0.])
        model.add_grid(3, [1., 0., 0.])
        model.add_grid(4, [0.5, 1., 0.])
        nids = [1, 2, 3, 4]
        model.add_cquad4(5, 5, nids, theta_mcid=0.0, zoffset=0., tflag=0,
                         T1=None, T2=None, T3=None, T4=None, comment='')
        model.add_pcomp(5, [mid], [0.1], thetas=None,
                        souts=None, nsm=0., sb=0., ft=None, tref=0., ge=0., lam=None, z0=None, comment='')

        E = 1.0E7
        G = None
        nu = 0.3
        model.add_mat1(mid, E, G, nu, rho=0.0, a=0.0, tref=0.0, ge=0.0,
                       St=0.0, Sc=0.0, Ss=0.0, mcsid=0, comment='')
        spc_id = 3
        load_id = 2
        components = '123456'
        nodes = [1, 2]
        model.add_spc1(spc_id, components, nodes, comment='')
        model.add_force(load_id, 3, 1.0, [0., 0., 1.], cid=0, comment='')
        model.add_force(load_id, 4, 1.0, [0., 0., 1.], cid=0, comment='')

        setup_case_control(model)
        solver = Solver(model)
        with self.assertRaises(RuntimeError):
            solver.run()
        #os.remove(model.bdf_filename)

    def test_cquad4_pshell_mat1(self):
        """Tests a CQUAD4/PSHELL/MAT1"""
        model = BDF(debug=True, log=None, mode='msc')
        model.bdf_filename = 'cquad4_pshell_mat1.bdf'
        model.add_grid(1, [0., 0., 0., ])
        model.add_grid(2, [1., 0., 0., ])
        model.add_grid(3, [1., 0., 2., ])
        model.add_grid(4, [0., 0., 2., ])
        mid = 3
        nids = [1, 2, 3, 4]
        model.add_cquad4(1, 1, nids, theta_mcid=0.0, zoffset=0., tflag=0,
                         T1=None, T2=None, T3=None, T4=None, comment='')
        model.add_cquad4(2, 2, nids, theta_mcid=0.0, zoffset=0., tflag=0,
                         T1=None, T2=None, T3=None, T4=None, comment='')
        model.add_cquad4(3, 3, nids, theta_mcid=0.0, zoffset=0., tflag=0,
                         T1=None, T2=None, T3=None, T4=None, comment='')
        model.add_cquad4(4, 4, nids, theta_mcid=0.0, zoffset=0., tflag=0,
                         T1=None, T2=None, T3=None, T4=None, comment='')
        model.add_cquad4(5, 5, nids, theta_mcid=0.0, zoffset=0., tflag=0,
                         T1=None, T2=None, T3=None, T4=None, comment='')

        model.add_pshell(1, mid1=mid, t=0.3, mid2=None, twelveIt3=1.0,
                         mid3=None, tst=0.833333, nsm=0.0, z1=None, z2=None,
                         mid4=None, comment='')
        model.add_pshell(2, mid1=None, t=0.3, mid2=mid, twelveIt3=1.0,
                         mid3=None, tst=0.833333, nsm=0.0, z1=None, z2=None,
                         mid4=None, comment='')
        model.add_pshell(3, mid1=None, t=0.3, mid2=None, twelveIt3=1.0,
                         mid3=mid, tst=0.833333, nsm=0.0, z1=None, z2=None,
                         mid4=None, comment='')
        model.add_pshell(4, mid1=None, t=0.3, mid2=None, twelveIt3=1.0,
                         mid3=None, tst=0.833333, nsm=0.0, z1=None, z2=None,
                         mid4=mid, comment='')
        model.add_pcomp(5, [mid], [0.1], thetas=None,
                        souts=None, nsm=0., sb=0., ft=None, tref=0., ge=0., lam=None, z0=None, comment='')

        E = 1.0E7
        G = None
        nu = 0.3
        model.add_mat1(mid, E, G, nu, rho=0.0, a=0.0, tref=0.0, ge=0.0,
                       St=0.0, Sc=0.0, Ss=0.0, mcsid=0, comment='')
        spc_id = 3
        load_id = 2
        components = '123456'
        nodes = [1, 2]
        model.add_spc1(spc_id, components, nodes, comment='')
        model.add_force(load_id, 3, 1.0, [0., 0., 1.], cid=0, comment='')
        model.add_force(load_id, 4, 1.0, [0., 0., 1.], cid=0, comment='')

        setup_case_control(model)
        solver = Solver(model)
        with self.assertRaises(RuntimeError):
            solver.run()
        #os.remove(model.bdf_filename)
        #os.remove(solver.f06_filename)
        #os.remove(solver.op2_filename)

if __name__ == '__main__':
    unittest.main()
