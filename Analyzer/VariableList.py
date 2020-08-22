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

Variables["lep0_pt"] = Variable()
Variables["lep0_pt"].varNameInTree = "lep0_pt"
Variables["lep0_pt"].xAxis = "lep0 p_{T} [GeV]"
Variables["lep0_pt"].yAxis = "Events"
Variables["lep0_pt"].doLogY = False
Variables["lep0_pt"].nbins = 500
Variables["lep0_pt"].xmin = 0
Variables["lep0_pt"].xmax = 500
Variables["lep0_pt"].rebins = []

Variables["lep0_eta"] = Variable()
Variables["lep0_eta"].varNameInTree = "lep0_eta"
Variables["lep0_eta"].xAxis = "lep0 #eta"
Variables["lep0_eta"].yAxis = "Events"
Variables["lep0_eta"].doLogY = False
Variables["lep0_eta"].nbins = etabins
Variables["lep0_eta"].xmin = etamin
Variables["lep0_eta"].xmax = etamax
Variables["lep0_eta"].rebins = []

Variables["lep0_phi"] = Variable()
Variables["lep0_phi"].varNameInTree = "lep0_phi"
Variables["lep0_phi"].xAxis = "lep0 #phi"
Variables["lep0_phi"].yAxis = "Events"
Variables["lep0_phi"].doLogY = False
Variables["lep0_phi"].nbins = phibins
Variables["lep0_phi"].xmin = phimin
Variables["lep0_phi"].xmax = phimax
Variables["lep0_phi"].rebins = []

Variables["lep0_mass"] = Variable()
Variables["lep0_mass"].varNameInTree = "lep0_mass"
Variables["lep0_mass"].xAxis = "lep0_mass [GeV]"
Variables["lep0_mass"].yAxis = "Events"
Variables["lep0_mass"].doLogY = False
Variables["lep0_mass"].nbins = 10
Variables["lep0_mass"].xmin = 0
Variables["lep0_mass"].xmax = 0.2
Variables["lep0_mass"].rebins = []

Variables["lep0_charge"] = Variable()
Variables["lep0_charge"].varNameInTree = "lep0_charge"
Variables["lep0_charge"].xAxis = "lep0_charge"
Variables["lep0_charge"].yAxis = "Events"
Variables["lep0_charge"].doLogY = False
Variables["lep0_charge"].nbins = 10
Variables["lep0_charge"].xmin = -2
Variables["lep0_charge"].xmax = 2
Variables["lep0_charge"].rebins = []

Variables["lep1_pt"] = Variable()
Variables["lep1_pt"].varNameInTree = "lep1_pt"
Variables["lep1_pt"].xAxis = "lep1 p_{T} [GeV]"
Variables["lep1_pt"].yAxis = "Events"
Variables["lep1_pt"].doLogY = False
Variables["lep1_pt"].nbins = 500
Variables["lep1_pt"].xmin = 0
Variables["lep1_pt"].xmax = 500
Variables["lep1_pt"].rebins = []

Variables["lep1_eta"] = Variable()
Variables["lep1_eta"].varNameInTree = "lep1_eta"
Variables["lep1_eta"].xAxis = "lep1 #eta"
Variables["lep1_eta"].yAxis = "Events"
Variables["lep1_eta"].doLogY = False
Variables["lep1_eta"].nbins = etabins
Variables["lep1_eta"].xmin = etamin
Variables["lep1_eta"].xmax = etamax
Variables["lep1_eta"].rebins = []

Variables["lep1_phi"] = Variable()
Variables["lep1_phi"].varNameInTree = "lep1_phi"
Variables["lep1_phi"].xAxis = "lep1 #phi"
Variables["lep1_phi"].yAxis = "Events"
Variables["lep1_phi"].doLogY = False
Variables["lep1_phi"].nbins = phibins
Variables["lep1_phi"].xmin = phimin
Variables["lep1_phi"].xmax = phimax
Variables["lep1_phi"].rebins = []

Variables["lep1_mass"] = Variable()
Variables["lep1_mass"].varNameInTree = "lep1_mass"
Variables["lep1_mass"].xAxis = "lep1_mass [GeV]"
Variables["lep1_mass"].yAxis = "Events"
Variables["lep1_mass"].doLogY = False
Variables["lep1_mass"].nbins = 10
Variables["lep1_mass"].xmin = 0
Variables["lep1_mass"].xmax = 0.2
Variables["lep1_mass"].rebins = []

Variables["lep1_charge"] = Variable()
Variables["lep1_charge"].varNameInTree = "lep1_charge"
Variables["lep1_charge"].xAxis = "lep1_charge"
Variables["lep1_charge"].yAxis = "Events"
Variables["lep1_charge"].doLogY = False
Variables["lep1_charge"].nbins = 10
Variables["lep1_charge"].xmin = -2
Variables["lep1_charge"].xmax = 2
Variables["lep1_charge"].rebins = []

Variables["dilep_pt"] = Variable()
Variables["dilep_pt"].varNameInTree = "dilep_pt"
Variables["dilep_pt"].xAxis = "dilep p_{T} [GeV]"
Variables["dilep_pt"].yAxis = "Events"
Variables["dilep_pt"].doLogY = False
Variables["dilep_pt"].nbins = 500
Variables["dilep_pt"].xmin = 0
Variables["dilep_pt"].xmax = 500
Variables["dilep_pt"].rebins = []

Variables["dilep_eta"] = Variable()
Variables["dilep_eta"].varNameInTree = "dilep_eta"
Variables["dilep_eta"].xAxis = "dilep #eta"
Variables["dilep_eta"].yAxis = "Events"
Variables["dilep_eta"].doLogY = False
Variables["dilep_eta"].nbins = etabins
Variables["dilep_eta"].xmin = etamin
Variables["dilep_eta"].xmax = etamax
Variables["dilep_eta"].rebins = []

Variables["dilep_phi"] = Variable()
Variables["dilep_phi"].varNameInTree = "dilep_phi"
Variables["dilep_phi"].xAxis = "dilep #phi"
Variables["dilep_phi"].yAxis = "Events"
Variables["dilep_phi"].doLogY = False
Variables["dilep_phi"].nbins = phibins
Variables["dilep_phi"].xmin = phimin
Variables["dilep_phi"].xmax = phimax
Variables["dilep_phi"].rebins = []

Variables["dilep_mass"] = Variable()
Variables["dilep_mass"].varNameInTree = "dilep_mass"
Variables["dilep_mass"].xAxis = "dilep_mass [GeV]"
Variables["dilep_mass"].yAxis = "Events"
Variables["dilep_mass"].doLogY = False
Variables["dilep_mass"].nbins = 80
Variables["dilep_mass"].xmin = 70
Variables["dilep_mass"].xmax = 110
Variables["dilep_mass"].rebins = []

Variables["nJetSel"] = Variable()
Variables["nJetSel"].varNameInTree = "nJetSel"
Variables["nJetSel"].xAxis = "# Jet Selected"
Variables["nJetSel"].yAxis = "Events"
Variables["nJetSel"].doLogY = False
Variables["nJetSel"].nbins = 10
Variables["nJetSel"].xmin = 0
Variables["nJetSel"].xmax = 10
Variables["nJetSel"].rebins = []

Variables["probeJet_pt"] = Variable()
Variables["probeJet_pt"].varNameInTree = "probeJet_pt"
Variables["probeJet_pt"].xAxis = "Jet0 p_{T} [GeV]"
Variables["probeJet_pt"].yAxis = "Events"
Variables["probeJet_pt"].doLogY = False
Variables["probeJet_pt"].nbins = 300
Variables["probeJet_pt"].xmin = 0
Variables["probeJet_pt"].xmax = 300
Variables["probeJet_pt"].rebins = []

Variables["probeJet_eta"] = Variable()
Variables["probeJet_eta"].varNameInTree = "probeJet_eta"
Variables["probeJet_eta"].xAxis = "Jet0 #eta"
Variables["probeJet_eta"].yAxis = "Events"
Variables["probeJet_eta"].doLogY = False
Variables["probeJet_eta"].nbins = etabins
Variables["probeJet_eta"].xmin = etamin
Variables["probeJet_eta"].xmax = etamax
Variables["probeJet_eta"].rebins = []

Variables["probeJet_phi"] = Variable()
Variables["probeJet_phi"].varNameInTree = "probeJet_phi"
Variables["probeJet_phi"].xAxis = "Jet0 #phi"
Variables["probeJet_phi"].yAxis = "Events"
Variables["probeJet_phi"].doLogY = False
Variables["probeJet_phi"].nbins = phibins
Variables["probeJet_phi"].xmin = phimin
Variables["probeJet_phi"].xmax = phimax
Variables["probeJet_phi"].rebins = []

Variables["probeJet_dilep_dphi"] = Variable()
Variables["probeJet_dilep_dphi"].varNameInTree = "probeJet_dilep_dphi"
Variables["probeJet_dilep_dphi"].xAxis = "#Delta#phi(dilep,probeJet)"
Variables["probeJet_dilep_dphi"].yAxis = "Events"
Variables["probeJet_dilep_dphi"].doLogY = False
Variables["probeJet_dilep_dphi"].nbins = 80
Variables["probeJet_dilep_dphi"].xmin = -4.0
Variables["probeJet_dilep_dphi"].xmax = 4.0
Variables["probeJet_dilep_dphi"].rebins = []

Variables["probeJet_dilep_dphi_norm"] = Variable()
Variables["probeJet_dilep_dphi_norm"].varNameInTree = "probeJet_dilep_dphi_norm"
Variables["probeJet_dilep_dphi_norm"].xAxis = "#Delta#phi(dilep,probeJet)/#pi"
Variables["probeJet_dilep_dphi_norm"].yAxis = "Events"
Variables["probeJet_dilep_dphi_norm"].doLogY = False
Variables["probeJet_dilep_dphi_norm"].nbins  = 100
Variables["probeJet_dilep_dphi_norm"].xmin =  0.0
Variables["probeJet_dilep_dphi_norm"].xmax =  2.0
Variables["probeJet_dilep_dphi_norm"].rebins = []
