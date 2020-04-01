float AbsDeltaPhi(float phi1, float phi2){
  // float dphi = phi1-phi2;
  // return fabs(dphi);

  float _phi1 = 0.0;
  float _phi2 = 0.0;
  if(phi1 > 0.0) _phi1 = phi1;
  if(phi1 < 0.0) {
    _phi1 = phi1 + (2*TMath::Pi());
  }
  if(phi2 > 0.0) _phi2 = phi2;
  if(phi2 < 0.0) {
    _phi2 = phi2 + (2*TMath::Pi());
  }
  return fabs(_phi1-_phi2);
}
float DeltaPhiNorm(float dphi){

  float _dphi = 0.0;
  if(dphi > 0.0) _dphi = dphi;
  if(dphi < 0.0) {
    _dphi = dphi + (2*TMath::Pi());
  }
  return _dphi/TMath::Pi();
}