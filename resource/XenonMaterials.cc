// XENON Header Files
#include "Xenon1tMaterials.hh"

// G4 Header Files
#include <G4Material.hh>
#include <G4NistManager.hh>
#include <G4SystemOfUnits.hh>

Xenon1tMaterials::Xenon1tMaterials() { ; }

Xenon1tMaterials::~Xenon1tMaterials() { ; }

void Xenon1tMaterials::DefineMaterials(
	G4double pWABSL = 1., 
	G4double pEPTFEReflectivity = 0.9935,
	G4double pGdConcentration = 0.2) {
  G4NistManager *pNistManager = G4NistManager::Instance();

  //========== Elements ==========
  G4Element *Xe = new G4Element("Xenon", "Xe", 54., 131.293 * g / mole);
  G4Element *H = new G4Element("Hydrogen", "H", 1., 1.0079 * g / mole);
  G4Element *C = new G4Element("Carbon", "C", 6., 12.011 * g / mole);
  G4Element *N = new G4Element("Nitrogen", "N", 7., 14.007 * g / mole);
  G4Element *O = new G4Element("Oxygen", "O", 8., 15.999 * g / mole);
  G4Element *F = new G4Element("Fluorine", "F", 9., 18.998 * g / mole);
  G4Element *Fe = new G4Element("Iron", "Fe", 26., 55.85 * g / mole);
  G4Element *Co = pNistManager->FindOrBuildElement("Co");

  //==== Air ====
  pNistManager->FindOrBuildMaterial("G4_AIR");
  G4Material *Air = G4Material::GetMaterial("G4_AIR");

  // Optical properties of air
  const G4int nEntries = 32;
  G4double PhotonEnergy[nEntries] = {
      2.034 * eV, 2.068 * eV, 2.103 * eV, 2.139 * eV, 2.177 * eV, 2.216 * eV,
      2.256 * eV, 2.298 * eV, 2.341 * eV, 2.386 * eV, 2.433 * eV, 2.481 * eV,
      2.532 * eV, 2.585 * eV, 2.640 * eV, 2.697 * eV, 2.757 * eV, 2.820 * eV,
      2.885 * eV, 2.954 * eV, 3.026 * eV, 3.102 * eV, 3.181 * eV, 3.265 * eV,
      3.353 * eV, 3.446 * eV, 3.545 * eV, 3.649 * eV, 3.760 * eV, 3.877 * eV,
      4.002 * eV, 4.136 * eV};

  G4double RefractiveIndex2[nEntries] = {
      1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00,
      1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00,
      1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00};
  G4MaterialPropertiesTable *myMPT2 = new G4MaterialPropertiesTable();
  myMPT2->AddProperty("RINDEX", PhotonEnergy, RefractiveIndex2, nEntries);
  Air->SetMaterialPropertiesTable(myMPT2);

  //==== Vacuum ====
  G4Material *Vacuum = new G4Material("Vacuum", 1.e-20 * g / cm3, 2, kStateGas);
  Vacuum->AddElement(N, 0.755);
  Vacuum->AddElement(O, 0.245);

  // Optical properties of vacuum
  G4double RefractiveIndex3[nEntries] = {
      1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00,
      1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00,
      1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00};
  G4MaterialPropertiesTable *myMPT3 = new G4MaterialPropertiesTable();
  myMPT3->AddProperty("RINDEX", PhotonEnergy, RefractiveIndex3, nEntries);
  Vacuum->SetMaterialPropertiesTable(myMPT3);

  //==== Steel ====
  G4Material *Steel = new G4Material("Steel", 7.7 * g / cm3, 3);
  Steel->AddElement(C, 0.04);
  Steel->AddElement(Fe, 0.88);
  Steel->AddElement(Co, 0.08);

  //==== Liquid Xenon ====
  G4Material *LXe = new G4Material("LXe", 2.862 * g / cm3, 1, kStateLiquid,
                                   177.05 * kelvin, 1.5 * atmosphere);
  LXe->AddElement(Xe, 1);

  // Optical properties LXe
  const G4int iNbEntries = 3;
  G4double pdLXePhotonMomentum[iNbEntries] = {6.91 * eV, 6.98 * eV, 7.05 * eV};
  G4double pdLXeScintillation[iNbEntries] = {0.1, 1.0, 0.1};
  G4double pdLXeRefractiveIndex[iNbEntries] = {1.63, 1.61, 1.58};
  G4double pdLXeAbsorbtionLength[iNbEntries] = {100. * cm, 100. * cm, 100. * cm};
  G4double pdLXeScatteringLength[iNbEntries] = {30. * cm, 30. * cm, 30. * cm};
  G4MaterialPropertiesTable *pLXePropertiesTable = new G4MaterialPropertiesTable();
  pLXePropertiesTable->AddProperty("FASTCOMPONENT", pdLXePhotonMomentum,
                                   pdLXeScintillation, iNbEntries);
  pLXePropertiesTable->AddProperty("SLOWCOMPONENT", pdLXePhotonMomentum,
                                   pdLXeScintillation, iNbEntries);
  pLXePropertiesTable->AddProperty("RINDEX", pdLXePhotonMomentum,
                                   pdLXeRefractiveIndex, iNbEntries);
  pLXePropertiesTable->AddProperty("ABSLENGTH", pdLXePhotonMomentum,
                                   pdLXeAbsorbtionLength, iNbEntries);
  pLXePropertiesTable->AddProperty("RAYLEIGH", pdLXePhotonMomentum,
                                   pdLXeScatteringLength, iNbEntries);
  pLXePropertiesTable->AddConstProperty("SCINTILLATIONYIELD", 0. / keV);
  pLXePropertiesTable->AddConstProperty("RESOLUTIONSCALE", 0);
  pLXePropertiesTable->AddConstProperty("FASTTIMECONSTANT", 3. * ns);
  pLXePropertiesTable->AddConstProperty("SLOWTIMECONSTANT", 27. * ns);
  pLXePropertiesTable->AddConstProperty("YIELDRATIO", 1.0);
  pLXePropertiesTable->AddConstProperty("TOTALNUM_INT_SITES", -1);
  LXe->SetMaterialPropertiesTable(pLXePropertiesTable);

  //==== Gaseous Xenon ====
  G4Material *GXe = new G4Material("GXe", 0.005887 * g / cm3, 1, kStateGas,
                                   173.15 * kelvin, 1.5 * atmosphere);
  GXe->AddElement(Xe, 1);

  // Optical properties GXe
  G4double pdGXePhotonMomentum[iNbEntries] = {6.91 * eV, 6.98 * eV, 7.05 * eV};
  G4double pdGXeScintillation[iNbEntries] = {0.1, 1.0, 0.1};
  G4double pdGXeRefractiveIndex[iNbEntries] = {1.00, 1.00, 1.00};
  G4double pdGXeAbsorbtionLength[iNbEntries] = {100 * m, 100 * m, 100 * m};
  G4double pdGXeScatteringLength[iNbEntries] = {100 * m, 100 * m, 100 * m};
  G4MaterialPropertiesTable *pGXePropertiesTable = new G4MaterialPropertiesTable();
  pGXePropertiesTable->AddProperty("FASTCOMPONENT", pdGXePhotonMomentum,
                                   pdGXeScintillation, iNbEntries);
  pGXePropertiesTable->AddProperty("SLOWCOMPONENT", pdGXePhotonMomentum,
                                   pdGXeScintillation, iNbEntries);
  pGXePropertiesTable->AddProperty("RINDEX", pdGXePhotonMomentum,
                                   pdGXeRefractiveIndex, iNbEntries);
  pGXePropertiesTable->AddProperty("ABSLENGTH", pdGXePhotonMomentum,
                                   pdGXeAbsorbtionLength, iNbEntries);
  pGXePropertiesTable->AddProperty("RAYLEIGH", pdGXePhotonMomentum,
                                   pdGXeScatteringLength, iNbEntries);
  pGXePropertiesTable->AddConstProperty("SCINTILLATIONYIELD", 0. / (keV));
  pGXePropertiesTable->AddConstProperty("RESOLUTIONSCALE", 0);
  pGXePropertiesTable->AddConstProperty("FASTTIMECONSTANT", 3. * ns);
  pGXePropertiesTable->AddConstProperty("SLOWTIMECONSTANT", 27. * ns);
  pGXePropertiesTable->AddConstProperty("YIELDRATIO", 1.0);
  GXe->SetMaterialPropertiesTable(pGXePropertiesTable);

  //==== Teflon ====
  G4Material *Teflon = new G4Material("Teflon", 2.2 * g / cm3, 2, kStateSolid);
  Teflon->AddElement(C, 0.240183);
  Teflon->AddElement(F, 0.759817);

  G4double pdTeflonPhotonMomentum[iNbEntries] = {6.91 * eV, 6.98 * eV, 7.05 * eV};
  G4double pdTeflonRefractiveIndex[iNbEntries] = {1.63, 1.61, 1.58};
  G4double pdTeflonReflectivity[iNbEntries] = {0.99, 0.99, 0.99};
  G4double pdTeflonSpecularLobe[iNbEntries] = {0.01, 0.01, 0.01};
  G4double pdTeflonSpecularSpike[iNbEntries] = {0.01, 0.01, 0.01};
  G4double pdTeflonBackscatter[iNbEntries] = {0.01, 0.01, 0.01};
  G4double pdTeflonEfficiency[iNbEntries] = {1.0, 1.0, 1.0};
  G4double pdTeflonAbsorbtionLength[iNbEntries] = {0.1 * cm, 0.1 * cm, 0.1 * cm};
  G4MaterialPropertiesTable *pTeflonPropertiesTable = new G4MaterialPropertiesTable();
  pTeflonPropertiesTable->AddProperty("RINDEX", pdTeflonPhotonMomentum,
                                      pdTeflonRefractiveIndex, iNbEntries);
  pTeflonPropertiesTable->AddProperty("REFLECTIVITY", pdTeflonPhotonMomentum,
                                      pdTeflonReflectivity, iNbEntries);
  pTeflonPropertiesTable->AddProperty("ABSLENGTH", pdTeflonPhotonMomentum,
                                      pdTeflonAbsorbtionLength, iNbEntries);
  pTeflonPropertiesTable->AddProperty("SPECULARLOBECONSTANT",
                                      pdTeflonPhotonMomentum,
                                      pdTeflonSpecularLobe, iNbEntries);
  pTeflonPropertiesTable->AddProperty("SPECULARSPIKECONSTANT",
                                      pdTeflonPhotonMomentum,
                                      pdTeflonSpecularSpike, iNbEntries);
  pTeflonPropertiesTable->AddProperty("BACKSCATTERCONSTANT",
                                      pdTeflonPhotonMomentum,
                                      pdTeflonBackscatter, iNbEntries);
  pTeflonPropertiesTable->AddProperty("EFFICIENCY", pdTeflonPhotonMomentum,
                                      pdTeflonEfficiency, iNbEntries);
  
  // Default optics if no OpticalSurface is given
  Teflon->SetMaterialPropertiesTable(pTeflonPropertiesTable);
  G4double pdTeflonSufraceTransmittance[iNbEntries] = {1e-12,1e-12,1e-12}; // 1e-12 because Geant4 is stupid
  
  //==== LXe Teflon Optical Surface ====
  pLXeTeflonOpticalSurface = new G4OpticalSurface("LXeTeflonOpticalSurface", 
       unified, ground, dielectric_dielectric, 0.1);

  G4MaterialPropertiesTable *pLXeTeflonPropertiesTable = new G4MaterialPropertiesTable();
  pLXeTeflonPropertiesTable->AddProperty("RINDEX", 
      pTeflonPropertiesTable->GetProperty("RINDEX"));
  pLXeTeflonPropertiesTable->AddProperty("REFLECTIVITY",
      pTeflonPropertiesTable->GetProperty("REFLECTIVITY"));
  pLXeTeflonPropertiesTable->AddProperty("ABSLENGTH", 
      pTeflonPropertiesTable->GetProperty("ABSLENGTH"));
  pLXeTeflonPropertiesTable->AddProperty("SPECULARLOBECONSTANT", 
      pTeflonPropertiesTable->GetProperty("SPECULARLOBECONSTANT"));
  pLXeTeflonPropertiesTable->AddProperty("SPECULARSPIKECONSTANT", 
      pTeflonPropertiesTable->GetProperty("SPECULARSPIKECONSTANT"));
  pLXeTeflonPropertiesTable->AddProperty("BACKSCATTERCONSTANT", 
      pTeflonPropertiesTable->GetProperty("BACKSCATTERCONSTANT"));
  pLXeTeflonPropertiesTable->AddProperty("EFFICIENCY", 
      pTeflonPropertiesTable->GetProperty("EFFICIENCY"));
  pLXeTeflonPropertiesTable->AddProperty("TRANSMITTANCE", pdTeflonPhotonMomentum, 
                                        pdTeflonSufraceTransmittance, iNbEntries);  
  pLXeTeflonOpticalSurface->SetMaterialPropertiesTable(pLXeTeflonPropertiesTable);
      
  //==== LXe Teflon Unpolished Optical Surface ====
  pLXeTeflonUnpolishedOpticalSurface = new G4OpticalSurface("LXeTeflonUnpolishedOpticalSurface", 
       unified, ground, dielectric_dielectric, 0.1);

  G4MaterialPropertiesTable *pLXeTeflonUnpolishedPropertiesTable = new G4MaterialPropertiesTable();
  pLXeTeflonUnpolishedPropertiesTable->AddProperty("RINDEX", 
      pTeflonPropertiesTable->GetProperty("RINDEX"));
  pLXeTeflonUnpolishedPropertiesTable->AddProperty("REFLECTIVITY",
      pTeflonPropertiesTable->GetProperty("REFLECTIVITY"));
  pLXeTeflonUnpolishedPropertiesTable->AddProperty("ABSLENGTH", 
      pTeflonPropertiesTable->GetProperty("ABSLENGTH"));
  pLXeTeflonUnpolishedPropertiesTable->AddProperty("SPECULARLOBECONSTANT", 
      pTeflonPropertiesTable->GetProperty("SPECULARLOBECONSTANT"));
  pLXeTeflonUnpolishedPropertiesTable->AddProperty("SPECULARSPIKECONSTANT", 
      pTeflonPropertiesTable->GetProperty("SPECULARSPIKECONSTANT"));
  pLXeTeflonUnpolishedPropertiesTable->AddProperty("BACKSCATTERCONSTANT", 
      pTeflonPropertiesTable->GetProperty("BACKSCATTERCONSTANT"));
  pLXeTeflonUnpolishedPropertiesTable->AddProperty("EFFICIENCY", 
      pTeflonPropertiesTable->GetProperty("EFFICIENCY"));
  pLXeTeflonUnpolishedPropertiesTable->AddProperty("TRANSMITTANCE", pdTeflonPhotonMomentum, 
                                        pdTeflonSufraceTransmittance, iNbEntries);         
  pLXeTeflonUnpolishedOpticalSurface->SetMaterialPropertiesTable(pLXeTeflonUnpolishedPropertiesTable);
  
  //==== GXe Teflon Optical Surface ====
  pGXeTeflonOpticalSurface = new G4OpticalSurface("GXeTeflonOpticalSurface", 
       unified, ground, dielectric_dielectric, 0.1);

  G4MaterialPropertiesTable *pGXeTeflonPropertiesTable = new G4MaterialPropertiesTable();
  pGXeTeflonPropertiesTable->AddProperty("RINDEX", 
      pTeflonPropertiesTable->GetProperty("RINDEX"));
  pGXeTeflonPropertiesTable->AddProperty("REFLECTIVITY",
      pTeflonPropertiesTable->GetProperty("REFLECTIVITY"));
  pGXeTeflonPropertiesTable->AddProperty("ABSLENGTH", 
      pTeflonPropertiesTable->GetProperty("ABSLENGTH"));
  pGXeTeflonPropertiesTable->AddProperty("SPECULARLOBECONSTANT", 
      pTeflonPropertiesTable->GetProperty("SPECULARLOBECONSTANT"));
  pGXeTeflonPropertiesTable->AddProperty("SPECULARSPIKECONSTANT", 
      pTeflonPropertiesTable->GetProperty("SPECULARSPIKECONSTANT"));
  pGXeTeflonPropertiesTable->AddProperty("BACKSCATTERCONSTANT", 
      pTeflonPropertiesTable->GetProperty("BACKSCATTERCONSTANT"));
  pGXeTeflonPropertiesTable->AddProperty("EFFICIENCY", 
      pTeflonPropertiesTable->GetProperty("EFFICIENCY"));
  pGXeTeflonPropertiesTable->AddProperty("TRANSMITTANCE", pdTeflonPhotonMomentum, 
                                        pdTeflonSufraceTransmittance, iNbEntries);         
  pGXeTeflonOpticalSurface->SetMaterialPropertiesTable(pGXeTeflonPropertiesTable);
  
  //==== GXe Teflon Unpolished Optical Surface ====
  pGXeTeflonUnpolishedOpticalSurface = new G4OpticalSurface("GXeTeflonUnpolishedOpticalSurface", 
       unified, ground, dielectric_dielectric, 0.1);

  G4MaterialPropertiesTable *pGXeUnpolishedTeflonPropertiesTable = new G4MaterialPropertiesTable();
  pGXeUnpolishedTeflonPropertiesTable->AddProperty("RINDEX", 
      pTeflonPropertiesTable->GetProperty("RINDEX"));
  pGXeUnpolishedTeflonPropertiesTable->AddProperty("REFLECTIVITY",
      pTeflonPropertiesTable->GetProperty("REFLECTIVITY"));
  pGXeUnpolishedTeflonPropertiesTable->AddProperty("ABSLENGTH", 
      pTeflonPropertiesTable->GetProperty("ABSLENGTH"));
  pGXeUnpolishedTeflonPropertiesTable->AddProperty("SPECULARLOBECONSTANT", 
      pTeflonPropertiesTable->GetProperty("SPECULARLOBECONSTANT"));
  pGXeUnpolishedTeflonPropertiesTable->AddProperty("SPECULARSPIKECONSTANT", 
      pTeflonPropertiesTable->GetProperty("SPECULARSPIKECONSTANT"));
  pGXeUnpolishedTeflonPropertiesTable->AddProperty("BACKSCATTERCONSTANT", 
      pTeflonPropertiesTable->GetProperty("BACKSCATTERCONSTANT"));
  pGXeUnpolishedTeflonPropertiesTable->AddProperty("EFFICIENCY", 
      pTeflonPropertiesTable->GetProperty("EFFICIENCY"));
  pGXeUnpolishedTeflonPropertiesTable->AddProperty("TRANSMITTANCE", pdTeflonPhotonMomentum, 
                                        pdTeflonSufraceTransmittance, iNbEntries);         
  pGXeTeflonUnpolishedOpticalSurface->SetMaterialPropertiesTable(pGXeUnpolishedTeflonPropertiesTable);
}

// Teflon reflectivity control functions
void Xenon1tMaterials::SetLXeTeflonReflectivity(G4double dReflectivity) {
    G4MaterialPropertiesTable *tmp = pLXeTeflonOpticalSurface->GetMaterialPropertiesTable();
    
    G4double teflon_PP[3] = {6.91 * eV, 6.98 * eV, 7.05 * eV};
    G4double teflon_REFL[3] = {dReflectivity, dReflectivity, dReflectivity};
    tmp->RemoveProperty("REFLECTIVITY");
	tmp->AddProperty("REFLECTIVITY", teflon_PP, teflon_REFL, 3);

	pLXeTeflonOpticalSurface->SetMaterialPropertiesTable(tmp);
	G4cout << "Xenon1tMaterials: Setting LXe/Teflon surface reflectivity to " << dReflectivity*100. << "%" << G4endl;    
}

void Xenon1tMaterials::SetGXeTeflonReflectivity(G4double dReflectivity) {
    G4MaterialPropertiesTable *tmp = pGXeTeflonOpticalSurface->GetMaterialPropertiesTable();
    
    G4double teflon_PP[3] = {6.91 * eV, 6.98 * eV, 7.05 * eV};
    G4double teflon_REFL[3] = {dReflectivity, dReflectivity, dReflectivity};
    tmp->RemoveProperty("REFLECTIVITY");
	tmp->AddProperty("REFLECTIVITY", teflon_PP, teflon_REFL, 3);

	pGXeTeflonOpticalSurface->SetMaterialPropertiesTable(tmp);
	G4cout << "Xenon1tMaterials: Setting GXe/Teflon surface reflectivity to " << dReflectivity*100. << "%" << G4endl;    
}

void Xenon1tMaterials::SetLXeTeflonUnpolishedReflectivity(G4double dReflectivity) {
    G4MaterialPropertiesTable *tmp = pLXeTeflonUnpolishedOpticalSurface->GetMaterialPropertiesTable();
    
    G4double teflon_PP[3] = {6.91 * eV, 6.98 * eV, 7.05 * eV};
    G4double teflon_REFL[3] = {dReflectivity, dReflectivity, dReflectivity};
    tmp->RemoveProperty("REFLECTIVITY");
	tmp->AddProperty("REFLECTIVITY", teflon_PP, teflon_REFL, 3);

	pLXeTeflonUnpolishedOpticalSurface->SetMaterialPropertiesTable(tmp);
	G4cout << "Xenon1tMaterials: Setting LXe/TeflonUnpolished surface reflectivity to " << dReflectivity*100. << "%" << G4endl;    
}

void Xenon1tMaterials::SetGXeTeflonUnpolishedReflectivity(G4double dReflectivity) {
    G4MaterialPropertiesTable *tmp = pGXeTeflonUnpolishedOpticalSurface->GetMaterialPropertiesTable();
    
    G4double teflon_PP[3] = {6.91 * eV, 6.98 * eV, 7.05 * eV};
    G4double teflon_REFL[3] = {dReflectivity, dReflectivity, dReflectivity};
    tmp->RemoveProperty("REFLECTIVITY");
	tmp->AddProperty("REFLECTIVITY", teflon_PP, teflon_REFL, 3);

	pGXeTeflonUnpolishedOpticalSurface->SetMaterialPropertiesTable(tmp);
	G4cout << "Xenon1tMaterials: Setting GXe/TeflonUnpolished surface reflectivity to " << dReflectivity*100. << "%" << G4endl;    
}

void Xenon1tMaterials::SetTeflonReflectivitySpikeLobeBackscatter(G4String type, G4ThreeVector parameters){
  G4MaterialPropertiesTable *tmp;
  if (type=="LXe"){tmp=pLXeTeflonOpticalSurface->GetMaterialPropertiesTable();}
  else if (type == "GXe" ){tmp=pGXeTeflonOpticalSurface->GetMaterialPropertiesTable();}
  else if (type == "LXeUnpolished"){tmp=pLXeTeflonUnpolishedOpticalSurface->GetMaterialPropertiesTable();}
  else if (type == "GXeUnpolished" ){tmp=pGXeTeflonUnpolishedOpticalSurface->GetMaterialPropertiesTable();}
  else { 
     G4cout << "Error! Unknown type for PTFE reflector : " << type << G4endl; 
     G4Exception("Xenon1tMaterials", "UknownPTFEtype",  FatalException, "Unknown type of reflector");
  }   
  G4double spike = parameters.x();
  G4double lobe = parameters.y();
  G4double backscatter = parameters.z();
  G4cout << type<<" Teflon reflectivity parameters:  "<<G4endl;
  G4cout << "          spike = "<< spike <<G4endl;
  G4cout << "           lobe = "<< lobe <<G4endl;
  G4cout << "    backscatter = "<< backscatter <<G4endl;
  if ( (spike + lobe + backscatter) > 1){
     G4cout << "ERROR! Total sum of components larger than 1" << G4endl;
     G4Exception("Xenon1tMaterials", "RuntimeErrors",  FatalException, "Total sum of reflection components is larger than 1"); }

  G4double pdTeflonPhotonMomentum[3] = {6.91 * eV, 6.98 * eV, 7.05 * eV};
  G4double pdSpecularSpike[3] = {spike,spike,spike};
  G4double pdSpecularLobe[3] = {lobe, lobe, lobe};
  G4double pdBackscatter[3] = {backscatter,backscatter,backscatter};
  
  tmp->RemoveProperty("SPECULARSPIKECONSTANT");
  tmp->AddProperty("SPECULARSPIKECONSTANT",
                   pdTeflonPhotonMomentum, pdSpecularSpike, 3 );
  tmp->RemoveProperty("SPECULARLOBECONSTANT");
  tmp->AddProperty("SPECULARLOBECONSTANT",
                   pdTeflonPhotonMomentum, pdSpecularLobe, 3 );
  tmp->RemoveProperty("BACKSCATTERCONSTANT");
  tmp->AddProperty("BACKSCATTERCONSTANT",
                   pdTeflonPhotonMomentum, pdBackscatter, 3 );
  
  if (type=="LXe"){pLXeTeflonOpticalSurface->SetMaterialPropertiesTable(tmp);}
  else if (type == "GXe" ){pGXeTeflonOpticalSurface->SetMaterialPropertiesTable(tmp);}
  else if (type =="LXeUnpolished"){pLXeTeflonUnpolishedOpticalSurface->SetMaterialPropertiesTable(tmp);}
  else if (type == "GXeUnpolished" ){pGXeTeflonUnpolishedOpticalSurface->SetMaterialPropertiesTable(tmp);}
  else { 
     G4cout << "Error! Unknown type for PTFE reflector : " << type << G4endl; 
     G4Exception("Xenon1tMaterials", "UknownPTFEtype",  FatalException, "Unknown type of reflector");
  } 
}

void Xenon1tMaterials::DumpTeflonSurfaceParameters(G4String type){
  G4MaterialPropertiesTable *tmp;
  if (type=="LXe"){tmp=pLXeTeflonOpticalSurface->GetMaterialPropertiesTable();}
  else if (type == "GXe" ){tmp=pGXeTeflonOpticalSurface->GetMaterialPropertiesTable();}
  else if (type =="LXeUnpolished"){tmp=pLXeTeflonUnpolishedOpticalSurface->GetMaterialPropertiesTable();}
  else if (type == "GXeUnpolished" ){tmp=pGXeTeflonUnpolishedOpticalSurface->GetMaterialPropertiesTable();}
  else { 
     G4cout << "Error! Unknown type for PTFE reflector : " << type << G4endl; 
     G4Exception("Xenon1tMaterials", "UknownPTFEtype",  FatalException, "Unknown type of reflector");
  }   
  G4cout << "All properties of Teflon suface type : " << type << G4endl;
  tmp->DumpTable();
}