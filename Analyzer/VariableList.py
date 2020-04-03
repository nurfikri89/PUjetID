import collections
import ROOT

class Variable:
  varNameInTree = ''
  xAxis = ''
  yAxis = ''
  nbins = 0
  xmin = 0
  xmax = 0
  doLogY = False
  rebins = []

etabins = 120
etamin = -6.0
etamax = 6.0

phibins = 80
phimin = -4.0
phimax = 4.0

njetbins = 12
njetmin = 0.
njetmax = 12.

pi = ROOT.TMath.Pi()

Variables = collections.OrderedDict()

Variables["mu0_pt"] = Variable()
Variables["mu0_pt"].varNameInTree = "mu0_pt"
Variables["mu0_pt"].xAxis = "mu0 p_{T} [GeV]"
Variables["mu0_pt"].yAxis = "Events"
Variables["mu0_pt"].doLogY = False
Variables["mu0_pt"].nbins = 500
Variables["mu0_pt"].xmin = 0
Variables["mu0_pt"].xmax = 500
Variables["mu0_pt"].rebins = []

Variables["mu0_eta"] = Variable()
Variables["mu0_eta"].varNameInTree = "mu0_eta"
Variables["mu0_eta"].xAxis = "mu0 #eta"
Variables["mu0_eta"].yAxis = "Events"
Variables["mu0_eta"].doLogY = False
Variables["mu0_eta"].nbins = etabins
Variables["mu0_eta"].xmin = etamin
Variables["mu0_eta"].xmax = etamax
Variables["mu0_eta"].rebins = []

Variables["mu0_phi"] = Variable()
Variables["mu0_phi"].varNameInTree = "mu0_phi"
Variables["mu0_phi"].xAxis = "mu0 #phi"
Variables["mu0_phi"].yAxis = "Events"
Variables["mu0_phi"].doLogY = False
Variables["mu0_phi"].nbins = phibins
Variables["mu0_phi"].xmin = phimin
Variables["mu0_phi"].xmax = phimax
Variables["mu0_phi"].rebins = []

Variables["mu0_mass"] = Variable()
Variables["mu0_mass"].varNameInTree = "mu0_mass"
Variables["mu0_mass"].xAxis = "mu0_mass [GeV]"
Variables["mu0_mass"].yAxis = "Events"
Variables["mu0_mass"].doLogY = False
Variables["mu0_mass"].nbins = 10
Variables["mu0_mass"].xmin = 0
Variables["mu0_mass"].xmax = 0.2
Variables["mu0_mass"].rebins = []

Variables["mu0_charge"] = Variable()
Variables["mu0_charge"].varNameInTree = "mu0_charge"
Variables["mu0_charge"].xAxis = "mu0_charge"
Variables["mu0_charge"].yAxis = "Events"
Variables["mu0_charge"].doLogY = False
Variables["mu0_charge"].nbins = 10
Variables["mu0_charge"].xmin = -2
Variables["mu0_charge"].xmax = 2
Variables["mu0_charge"].rebins = []

Variables["mu1_pt"] = Variable()
Variables["mu1_pt"].varNameInTree = "mu1_pt"
Variables["mu1_pt"].xAxis = "mu1 p_{T} [GeV]"
Variables["mu1_pt"].yAxis = "Events"
Variables["mu1_pt"].doLogY = False
Variables["mu1_pt"].nbins = 500
Variables["mu1_pt"].xmin = 0
Variables["mu1_pt"].xmax = 500
Variables["mu1_pt"].rebins = []

Variables["mu1_eta"] = Variable()
Variables["mu1_eta"].varNameInTree = "mu1_eta"
Variables["mu1_eta"].xAxis = "mu1 #eta"
Variables["mu1_eta"].yAxis = "Events"
Variables["mu1_eta"].doLogY = False
Variables["mu1_eta"].nbins = etabins
Variables["mu1_eta"].xmin = etamin
Variables["mu1_eta"].xmax = etamax
Variables["mu1_eta"].rebins = []

Variables["mu1_phi"] = Variable()
Variables["mu1_phi"].varNameInTree = "mu1_phi"
Variables["mu1_phi"].xAxis = "mu1 #phi"
Variables["mu1_phi"].yAxis = "Events"
Variables["mu1_phi"].doLogY = False
Variables["mu1_phi"].nbins = phibins
Variables["mu1_phi"].xmin = phimin
Variables["mu1_phi"].xmax = phimax
Variables["mu1_phi"].rebins = []

Variables["mu1_mass"] = Variable()
Variables["mu1_mass"].varNameInTree = "mu1_mass"
Variables["mu1_mass"].xAxis = "mu1_mass [GeV]"
Variables["mu1_mass"].yAxis = "Events"
Variables["mu1_mass"].doLogY = False
Variables["mu1_mass"].nbins = 10
Variables["mu1_mass"].xmin = 0
Variables["mu1_mass"].xmax = 0.2
Variables["mu1_mass"].rebins = []

Variables["mu1_charge"] = Variable()
Variables["mu1_charge"].varNameInTree = "mu1_charge"
Variables["mu1_charge"].xAxis = "mu1_charge"
Variables["mu1_charge"].yAxis = "Events"
Variables["mu1_charge"].doLogY = False
Variables["mu1_charge"].nbins = 10
Variables["mu1_charge"].xmin = -2
Variables["mu1_charge"].xmax = 2
Variables["mu1_charge"].rebins = []

Variables["dimuon_pt"] = Variable()
Variables["dimuon_pt"].varNameInTree = "dimuon_pt"
Variables["dimuon_pt"].xAxis = "dimuon p_{T} [GeV]"
Variables["dimuon_pt"].yAxis = "Events"
Variables["dimuon_pt"].doLogY = False
Variables["dimuon_pt"].nbins = 500
Variables["dimuon_pt"].xmin = 0
Variables["dimuon_pt"].xmax = 500
Variables["dimuon_pt"].rebins = []

Variables["dimuon_eta"] = Variable()
Variables["dimuon_eta"].varNameInTree = "dimuon_eta"
Variables["dimuon_eta"].xAxis = "dimuon #eta"
Variables["dimuon_eta"].yAxis = "Events"
Variables["dimuon_eta"].doLogY = False
Variables["dimuon_eta"].nbins = etabins
Variables["dimuon_eta"].xmin = etamin
Variables["dimuon_eta"].xmax = etamax
Variables["dimuon_eta"].rebins = []

Variables["dimuon_phi"] = Variable()
Variables["dimuon_phi"].varNameInTree = "dimuon_phi"
Variables["dimuon_phi"].xAxis = "dimuon #phi"
Variables["dimuon_phi"].yAxis = "Events"
Variables["dimuon_phi"].doLogY = False
Variables["dimuon_phi"].nbins = phibins
Variables["dimuon_phi"].xmin = phimin
Variables["dimuon_phi"].xmax = phimax
Variables["dimuon_phi"].rebins = []

Variables["dimuon_mass"] = Variable()
Variables["dimuon_mass"].varNameInTree = "dimuon_mass"
Variables["dimuon_mass"].xAxis = "dimuon_mass [GeV]"
Variables["dimuon_mass"].yAxis = "Events"
Variables["dimuon_mass"].doLogY = False
Variables["dimuon_mass"].nbins = 80
Variables["dimuon_mass"].xmin = 70
Variables["dimuon_mass"].xmax = 110
Variables["dimuon_mass"].rebins = []

Variables["nJetSel"] = Variable()
Variables["nJetSel"].varNameInTree = "nJetSel"
Variables["nJetSel"].xAxis = "# Jet Selected"
Variables["nJetSel"].yAxis = "Events"
Variables["nJetSel"].doLogY = False
Variables["nJetSel"].nbins = 10
Variables["nJetSel"].xmin = 0
Variables["nJetSel"].xmax = 10
Variables["nJetSel"].rebins = []

Variables["jet0_pt"] = Variable()
Variables["jet0_pt"].varNameInTree = "jet0_pt"
Variables["jet0_pt"].xAxis = "Jet0 p_{T} [GeV]"
Variables["jet0_pt"].yAxis = "Events"
Variables["jet0_pt"].doLogY = False
Variables["jet0_pt"].nbins = 300
Variables["jet0_pt"].xmin = 0
Variables["jet0_pt"].xmax = 300
Variables["jet0_pt"].rebins = []

Variables["jet0_eta"] = Variable()
Variables["jet0_eta"].varNameInTree = "jet0_eta"
Variables["jet0_eta"].xAxis = "Jet0 #eta"
Variables["jet0_eta"].yAxis = "Events"
Variables["jet0_eta"].doLogY = False
Variables["jet0_eta"].nbins = etabins
Variables["jet0_eta"].xmin = etamin
Variables["jet0_eta"].xmax = etamax
Variables["jet0_eta"].rebins = []

Variables["jet0_phi"] = Variable()
Variables["jet0_phi"].varNameInTree = "jet0_phi"
Variables["jet0_phi"].xAxis = "Jet0 #phi"
Variables["jet0_phi"].yAxis = "Events"
Variables["jet0_phi"].doLogY = False
Variables["jet0_phi"].nbins = phibins
Variables["jet0_phi"].xmin = phimin
Variables["jet0_phi"].xmax = phimax
Variables["jet0_phi"].rebins = []

Variables["jet0_dimuon_dphi"] = Variable()
Variables["jet0_dimuon_dphi"].varNameInTree = "jet0_dimuon_dphi"
Variables["jet0_dimuon_dphi"].xAxis = "#Delta#phi(dimuon,jet0)"
Variables["jet0_dimuon_dphi"].yAxis = "Events"
Variables["jet0_dimuon_dphi"].doLogY = False
Variables["jet0_dimuon_dphi"].nbins = 80
Variables["jet0_dimuon_dphi"].xmin = -4.0
Variables["jet0_dimuon_dphi"].xmax = 4.0
Variables["jet0_dimuon_dphi"].rebins = []

Variables["jet0_dimuon_dphi_norm"] = Variable()
Variables["jet0_dimuon_dphi_norm"].varNameInTree = "jet0_dimuon_dphi_norm"
Variables["jet0_dimuon_dphi_norm"].xAxis = "#Delta#phi(dimuon,jet0)/#pi"
Variables["jet0_dimuon_dphi_norm"].yAxis = "Events"
Variables["jet0_dimuon_dphi_norm"].doLogY = False
Variables["jet0_dimuon_dphi_norm"].nbins  = 100
Variables["jet0_dimuon_dphi_norm"].xmin =  0.0
Variables["jet0_dimuon_dphi_norm"].xmax =  2.0
Variables["jet0_dimuon_dphi_norm"].rebins = []
