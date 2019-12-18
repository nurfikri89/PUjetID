import collections
import ROOT
from numpy import array

etabins = 120;
etamin = -6.0;
etamax = 6.0;

phibins = 80;
phimin = -4.0;
phimax = 4.0;

njetbins = 12;
njetmin = 0.;
njetmax = 12.;

class Variable:
	varNameInTree = ''
	xAxisName = ''
	yAxisName = ''
	nbins = 0
	xmin = 0
	xmax = 0
	doLogY = False
	rebins = []

Variables = collections.OrderedDict()

# Variables["mu0_pt"] = Variable()
# Variables["mu0_pt"].varNameInTree = "mu0_pt"
# Variables["mu0_pt"].xAxisName = "mu0 p_{T} [GeV]"
# Variables["mu0_pt"].yAxisName = "Events"
# Variables["mu0_pt"].doLogY = False
# Variables["mu0_pt"].nbins = 500
# Variables["mu0_pt"].xmin = 0
# Variables["mu0_pt"].xmax = 500
# Variables["mu0_pt"].rebins = []

# Variables["mu0_eta"] = Variable()
# Variables["mu0_eta"].varNameInTree = "mu0_eta"
# Variables["mu0_eta"].xAxisName = "mu0 #eta"
# Variables["mu0_eta"].yAxisName = "Events"
# Variables["mu0_eta"].doLogY = False
# Variables["mu0_eta"].nbins = etabins
# Variables["mu0_eta"].xmin = etamin
# Variables["mu0_eta"].xmax = etamax
# Variables["mu0_eta"].rebins = []

# Variables["mu0_phi"] = Variable()
# Variables["mu0_phi"].varNameInTree = "mu0_phi"
# Variables["mu0_phi"].xAxisName = "mu0 #phi"
# Variables["mu0_phi"].yAxisName = "Events"
# Variables["mu0_phi"].doLogY = False
# Variables["mu0_phi"].nbins = phibins
# Variables["mu0_phi"].xmin = phimin
# Variables["mu0_phi"].xmax = phimax
# Variables["mu0_phi"].rebins = []

# Variables["mu0_mass"] = Variable()
# Variables["mu0_mass"].varNameInTree = "mu0_mass"
# Variables["mu0_mass"].xAxisName = "mu0_mass [GeV]"
# Variables["mu0_mass"].yAxisName = "Events"
# Variables["mu0_mass"].doLogY = False
# Variables["mu0_mass"].nbins = 10
# Variables["mu0_mass"].xmin = 0
# Variables["mu0_mass"].xmax = 0.2
# Variables["mu0_mass"].rebins = []

# Variables["mu0_charge"] = Variable()
# Variables["mu0_charge"].varNameInTree = "mu0_charge"
# Variables["mu0_charge"].xAxisName = "mu0_charge"
# Variables["mu0_charge"].yAxisName = "Events"
# Variables["mu0_charge"].doLogY = False
# Variables["mu0_charge"].nbins = 10
# Variables["mu0_charge"].xmin = -2
# Variables["mu0_charge"].xmax = 2
# Variables["mu0_charge"].rebins = []

# Variables["mu1_pt"] = Variable()
# Variables["mu1_pt"].varNameInTree = "mu1_pt"
# Variables["mu1_pt"].xAxisName = "mu1 p_{T} [GeV]"
# Variables["mu1_pt"].yAxisName = "Events"
# Variables["mu1_pt"].doLogY = False
# Variables["mu1_pt"].nbins = 500
# Variables["mu1_pt"].xmin = 0
# Variables["mu1_pt"].xmax = 500
# Variables["mu1_pt"].rebins = []

# Variables["mu1_eta"] = Variable()
# Variables["mu1_eta"].varNameInTree = "mu1_eta"
# Variables["mu1_eta"].xAxisName = "mu1 #eta"
# Variables["mu1_eta"].yAxisName = "Events"
# Variables["mu1_eta"].doLogY = False
# Variables["mu1_eta"].nbins = etabins
# Variables["mu1_eta"].xmin = etamin
# Variables["mu1_eta"].xmax = etamax
# Variables["mu1_eta"].rebins = []

# Variables["mu1_phi"] = Variable()
# Variables["mu1_phi"].varNameInTree = "mu1_phi"
# Variables["mu1_phi"].xAxisName = "mu1 #phi"
# Variables["mu1_phi"].yAxisName = "Events"
# Variables["mu1_phi"].doLogY = False
# Variables["mu1_phi"].nbins = phibins
# Variables["mu1_phi"].xmin = phimin
# Variables["mu1_phi"].xmax = phimax
# Variables["mu1_phi"].rebins = []

# Variables["mu1_mass"] = Variable()
# Variables["mu1_mass"].varNameInTree = "mu1_mass"
# Variables["mu1_mass"].xAxisName = "mu1_mass [GeV]"
# Variables["mu1_mass"].yAxisName = "Events"
# Variables["mu1_mass"].doLogY = False
# Variables["mu1_mass"].nbins = 10
# Variables["mu1_mass"].xmin = 0
# Variables["mu1_mass"].xmax = 0.2
# Variables["mu1_mass"].rebins = []

# Variables["mu1_charge"] = Variable()
# Variables["mu1_charge"].varNameInTree = "mu1_charge"
# Variables["mu1_charge"].xAxisName = "mu1_charge"
# Variables["mu1_charge"].yAxisName = "Events"
# Variables["mu1_charge"].doLogY = False
# Variables["mu1_charge"].nbins = 10
# Variables["mu1_charge"].xmin = -2
# Variables["mu1_charge"].xmax = 2
# Variables["mu1_charge"].rebins = []

# Variables["dimuon_pt"] = Variable()
# Variables["dimuon_pt"].varNameInTree = "dimuon_pt"
# Variables["dimuon_pt"].xAxisName = "dimuon p_{T} [GeV]"
# Variables["dimuon_pt"].yAxisName = "Events"
# Variables["dimuon_pt"].doLogY = False
# Variables["dimuon_pt"].nbins = 500
# Variables["dimuon_pt"].xmin = 0
# Variables["dimuon_pt"].xmax = 500
# Variables["dimuon_pt"].rebins = []

# Variables["dimuon_eta"] = Variable()
# Variables["dimuon_eta"].varNameInTree = "dimuon_eta"
# Variables["dimuon_eta"].xAxisName = "dimuon #eta"
# Variables["dimuon_eta"].yAxisName = "Events"
# Variables["dimuon_eta"].doLogY = False
# Variables["dimuon_eta"].nbins = etabins
# Variables["dimuon_eta"].xmin = etamin
# Variables["dimuon_eta"].xmax = etamax
# Variables["dimuon_eta"].rebins = []

# Variables["dimuon_phi"] = Variable()
# Variables["dimuon_phi"].varNameInTree = "dimuon_phi"
# Variables["dimuon_phi"].xAxisName = "dimuon #phi"
# Variables["dimuon_phi"].yAxisName = "Events"
# Variables["dimuon_phi"].doLogY = False
# Variables["dimuon_phi"].nbins = phibins
# Variables["dimuon_phi"].xmin = phimin
# Variables["dimuon_phi"].xmax = phimax
# Variables["dimuon_phi"].rebins = []

# Variables["dimuon_mass"] = Variable()
# Variables["dimuon_mass"].varNameInTree = "dimuon_mass"
# Variables["dimuon_mass"].xAxisName = "dimuon_mass [GeV]"
# Variables["dimuon_mass"].yAxisName = "Events"
# Variables["dimuon_mass"].doLogY = False
# Variables["dimuon_mass"].nbins = 80
# Variables["dimuon_mass"].xmin = 70
# Variables["dimuon_mass"].xmax = 110
# Variables["dimuon_mass"].rebins = []

# Variables["nJetSel"] = Variable()
# Variables["nJetSel"].varNameInTree = "nJetSel"
# Variables["nJetSel"].xAxisName = "# Jet Selected"
# Variables["nJetSel"].yAxisName = "Events"
# Variables["nJetSel"].doLogY = False
# Variables["nJetSel"].nbins = 10
# Variables["nJetSel"].xmin = 0
# Variables["nJetSel"].xmax = 10
# Variables["nJetSel"].rebins = []

# Variables["jet0_pt"] = Variable()
# Variables["jet0_pt"].varNameInTree = "jet0_pt"
# Variables["jet0_pt"].xAxisName = "Jet0 p_{T} [GeV]"
# Variables["jet0_pt"].yAxisName = "Events"
# Variables["jet0_pt"].doLogY = False
# Variables["jet0_pt"].nbins = 300
# Variables["jet0_pt"].xmin = 0
# Variables["jet0_pt"].xmax = 300
# Variables["jet0_pt"].rebins = []

# Variables["jet0_eta"] = Variable()
# Variables["jet0_eta"].varNameInTree = "jet0_eta"
# Variables["jet0_eta"].xAxisName = "Jet0 #eta"
# Variables["jet0_eta"].yAxisName = "Events"
# Variables["jet0_eta"].doLogY = False
# Variables["jet0_eta"].nbins = etabins
# Variables["jet0_eta"].xmin = etamin
# Variables["jet0_eta"].xmax = etamax
# Variables["jet0_eta"].rebins = []

# Variables["jet0_phi"] = Variable()
# Variables["jet0_phi"].varNameInTree = "jet0_phi"
# Variables["jet0_phi"].xAxisName = "Jet0 #phi"
# Variables["jet0_phi"].yAxisName = "Events"
# Variables["jet0_phi"].doLogY = False
# Variables["jet0_phi"].nbins = phibins
# Variables["jet0_phi"].xmin = phimin
# Variables["jet0_phi"].xmax = phimax
# Variables["jet0_phi"].rebins = []

pi = ROOT.TMath.Pi()
Variables["jet0_dimuon_dphi"] = Variable()
Variables["jet0_dimuon_dphi"].varNameInTree = "jet0_dimuon_dphi"
Variables["jet0_dimuon_dphi"].xAxisName = "#Delta#phi(dimuon,jet0)"
Variables["jet0_dimuon_dphi"].yAxisName = "Events"
Variables["jet0_dimuon_dphi"].doLogY = False
Variables["jet0_dimuon_dphi"].nbins = 80
Variables["jet0_dimuon_dphi"].xmin = -4.0
Variables["jet0_dimuon_dphi"].xmax = 4.0
Variables["jet0_dimuon_dphi"].rebins = []

Variables["jet0_dimuon_dphi_norm"] = Variable()
Variables["jet0_dimuon_dphi_norm"].varNameInTree = "jet0_dimuon_dphi_norm"
Variables["jet0_dimuon_dphi_norm"].xAxisName = "#Delta#phi(dimuon,jet0)/#pi"
Variables["jet0_dimuon_dphi_norm"].yAxisName = "Events"
Variables["jet0_dimuon_dphi_norm"].doLogY = False
Variables["jet0_dimuon_dphi_norm"].nbins = 100
Variables["jet0_dimuon_dphi_norm"].xmin =  0.0
Variables["jet0_dimuon_dphi_norm"].xmax =  2.0
Variables["jet0_dimuon_dphi_norm"].rebins = []

