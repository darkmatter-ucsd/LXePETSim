// XENON Header Files
#include "Xenon1tPhysicsList.hh"
#include "Xenon1tPhysicsMessenger.hh"
#include <Xenon1tOpBoundaryProcess.hh>
#include <Xenon1tOpticalPhysics.hh>

// Additional Header Files
#include <globals.hh>
#include <iomanip>
#include <vector>

// Geant4 headers
#include "G4SystemOfUnits.hh"
#include "G4UnitsTable.hh"

#include <G4DecayPhysics.hh>
#include <G4EmCalculator.hh>
#include <G4EmExtraPhysics.hh>
#include <G4EmPenelopePhysics.hh>
#include <G4EmStandardPhysics.hh>
#include <G4HadronicProcessStore.hh>
#include <G4NistManager.hh>
#include <Xenon1tOpticalPhysics.hh>
#include <G4StoppingPhysics.hh>
#include <G4ios.hh>

#include "G4HadronElasticPhysicsHP.hh"
#include "G4HadronInelasticQBBC.hh"
#include "G4HadronPhysicsFTFP_BERT_HP.hh"
#include "G4HadronPhysicsINCLXX.hh"
#include "G4HadronPhysicsQGSP_BERT.hh"
#include "G4HadronPhysicsQGSP_BERT_HP.hh"
#include "G4HadronPhysicsQGSP_BIC_HP.hh"
#include "G4HadronPhysicsQGSP_BIC.hh"
#include "G4HadronPhysicsShielding.hh"
#include "G4IonElasticPhysics.hh"
#include "G4IonINCLXXPhysics.hh"
#include "G4IonPhysics.hh"

#include "G4EmLivermorePhysics.hh"
#include "G4PhysListFactory.hh"
#include "G4RadioactiveDecayPhysics.hh"
#include "G4NuclideTable.hh"
#include "G4VModularPhysicsList.hh"
#include "G4BuilderType.hh"

// Neutron capture header
#include "SKNeutronCapturePhysics.hh"

Xenon1tPhysicsList::Xenon1tPhysicsList()
    : G4VModularPhysicsList() {
  VerboseLevel = 0;
  OpVerbLevel = 0;
  SetVerboseLevel(VerboseLevel);

  //defaultCutValue = 1.0 * mm;
  //cutForGamma = defaultCutValue;
  //cutForElectron = defaultCutValue;
  //cutForPositron = defaultCutValue;
  //cutForProton   = defaultCutValue;

  m_pMessenger = new Xenon1tPhysicsMessenger(this);

  /// Xenon1tOpticalPhysics
  //  creates the following particles:
  //     bosons:  G4OpticalPhoton
  //
  //  and adds the following physical processes to these particles:
  //     G4OpAbsorption, G4OpRayleigh, G4OpMieHG, G4OpBoundaryProcess, G4OpWLS,
  //     G4Scintillation, G4Cerenkov
  RegisterPhysics(OpticalPhysicsModel = new Xenon1tOpticalPhysics(VerboseLevel));
  ((Xenon1tOpticalPhysics *)OpticalPhysicsModel)->SetMaxNumPhotonsPerStep(1000);
  ((Xenon1tOpticalPhysics *)OpticalPhysicsModel)->SetMaxBetaChangePerStep(10);
  ((Xenon1tOpticalPhysics *)OpticalPhysicsModel)->SetTrackSecondariesFirst(kCerenkov, true);
  ((Xenon1tOpticalPhysics *)OpticalPhysicsModel)->Configure(kCerenkov, false);

  // Hadron Elastic scattering
  RegisterPhysics(new G4HadronElasticPhysicsHP(VerboseLevel));

  // Hadron Inelastic Physics
  auto HadronInelasticPhysics = new G4HadronPhysicsQGSP_BERT(VerboseLevel);
  //auto HadronInelasticPhysics = new G4HadronPhysicsShielding(VerboseLevel);
  //auto HadronInelasticPhysics = new G4HadronStoppingProcess(VerboseLevel); // may not work

  // Before registration, Physics type should be set to replace that later.
  // This should be set for hadron physics, not for electromagnetic physics.
  HadronInelasticPhysics->SetPhysicsType(bHadronInelastic);
  RegisterPhysics(HadronInelasticPhysics);

  // Neutron Capture Physics developed by SK Collaboration
  RegisterPhysics( new SKNeutronCapturePhysics(VerboseLevel, "neutron") );

  // Ion Elastic scattering
  RegisterPhysics(new G4IonElasticPhysics(VerboseLevel));

  // Ion Inelastic Physics
  RegisterPhysics(new G4IonPhysics(VerboseLevel));
  ////RegisterPhysics( new G4IonINCLXXPhysics(VerboseLevel));

  // Gamma-Nuclear Physics - see Hadr03
  // RegisterPhysics( new GammaPhysics("gamma") );

  // EM physics
  /// G4EmStandardPhysics
  //  creates the following particles:
  //     bosons:  G4Gamma
  //     leptons: G4Electron, G4Positron, G4MuonPlus, G4MuonMinus
  //     mesons:  G4PionPlus, G4PionMinus, G4KaonPlus, G4KaonMinus
  //     baryons: G4Proton, G4AntiProton
  //     ions:    G4Deuteron, G4Triton, G4He3, G4Alpha, G4GenericIon
  //
  //  and adds the following physical processes to these particles:
  //     G4ComptonScattering, G4GammaConversion, G4PhotoElectricEffect
  //     G4eMultipleScattering, G4eIonisation, G4eBremsstrahlung,
  //     G4eplusAnnihilation
  //     G4MuMultipleScattering, G4MuIonisation, G4MuBremsstrahlung,
  //     G4MuPairProduction
  //     G4CoulombScattering
  //     G4hMultipleScattering, G4hBremsstrahlung, G4hIonisation,
  //     G4hPairProduction
  //     G4ionIonisation
  RegisterPhysics(new G4EmStandardPhysics(VerboseLevel, ""));

  /// G4EmExtraPhysics
  //  creates the following particles:
  //     bosons:  G4Gamma
  //     leptons: G4Electron, G4Positron, G4MuonPlus, G4MuonMinus
  //
  //  and adds the following physical processes to these particles:
  //     G4SynchrotronRadiation, G4MuNuclearInteraction, G4ElectroNuclearBuilder
  RegisterPhysics(new G4EmExtraPhysics(VerboseLevel));

  // Decay
  /// G4DecayPhysics
  //  creates the following particles:
  //     bosons:     G4BosonConstructor
  //     leptons:    G4LeptonConstructor
  //     mesons:     G4MesonConstructor
  //     baryons:    G4BaryonConstructor
  //     ions:       G4IonConstructor
  //     resonances: G4ShortLivedConstructor
  //
  //  and adds the following physical processes to these particles:
  //     G4Decay
  RegisterPhysics(new G4DecayPhysics(VerboseLevel));

  // Radioactive decay
  RegisterPhysics(new G4RadioactiveDecayPhysics(VerboseLevel));
  G4NuclideTable::GetInstance()->SetThresholdOfHalfLife(1*nanosecond);
  G4NuclideTable::GetInstance()->SetLevelTolerance(1.0*eV);

  /// G4StoppingPhysics
  //  like G4CaptureAtRestPhysics, but uses G4MuonMinusCaptureAtRest for muons
  RegisterPhysics(new G4StoppingPhysics(VerboseLevel));
}

void Xenon1tPhysicsList::SetCerenkov(G4bool useCerenkov) {
  ((Xenon1tOpticalPhysics *)OpticalPhysicsModel)->Configure(kCerenkov, useCerenkov);
    G4cout << "Xenon1tPhysicsList::SetCerenkov(): "
         << useCerenkov << G4endl;
}

void Xenon1tPhysicsList::SetEMlowEnergyModel(G4String name) {
    if (name == "emstandard") {
    ReplacePhysics(new G4EmStandardPhysics(VerboseLevel, ""));
  } else if (name == "emlivermore") {
    ReplacePhysics(new G4EmLivermorePhysics(VerboseLevel, ""));
  } else if (name == "empenelope") {
    ReplacePhysics(new G4EmPenelopePhysics(VerboseLevel, ""));
  } else {
    G4cout << "Xenon1tPhysicsList::Xenon1tPhysicsList() FATAL: Bad EM physics "
              "list chosen: " << name << G4endl;
    G4String msg =
        " Available choices are: <emstandard> <emlivermore "
        "(default)> <empenelope>";
    G4Exception("Xenon1tPhysicsList::Xenon1tPhysicsList()", "PhysicsList",
                FatalException, msg);
  }
  G4cout << "Xenon1tPhysicsList::SetEMlowEnergyModel(): "
         << name << G4endl;
}

void Xenon1tPhysicsList::SetHadronicModel(G4String name) {
  // Hadron Inelastic Physics
  G4VPhysicsConstructor* HadronInelasticPhysics = nullptr;
  if (name == "QGSP_BIC_HP") {
      HadronInelasticPhysics = new G4HadronPhysicsQGSP_BIC_HP(VerboseLevel);
  } else if (name == "QGSP_BIC") {
      HadronInelasticPhysics = new G4HadronPhysicsQGSP_BIC(VerboseLevel);
  } else if (name == "FTFP_BERT_HP") {
      HadronInelasticPhysics = new G4HadronPhysicsFTFP_BERT_HP(VerboseLevel);
  } else if (name == "QBBC") {
      HadronInelasticPhysics = new G4HadronInelasticQBBC(VerboseLevel);
  } else if (name == "INCLXX") {
      HadronInelasticPhysics = new G4HadronPhysicsINCLXX(VerboseLevel);
  } else if (name == "QGSP_BERT_HP") {
      HadronInelasticPhysics = new G4HadronPhysicsQGSP_BERT_HP(VerboseLevel);
  } else if (name == "QGSP_BERT") {
      HadronInelasticPhysics = new G4HadronPhysicsQGSP_BERT(VerboseLevel);
  } else if (name == "Shielding") {
      HadronInelasticPhysics = new G4HadronPhysicsShielding(VerboseLevel);
  }
   else {
    G4String msg =
        "Xenon1tPhysicsList::Xenon1tPhysicsList() Available choices "
        "for Hadronic Physics are: <QGSP_BIC_HP> <QGSP_BERT_HP> "
        "<FTFP_BERT_HP> <QBBC> <QGSP_BERT> <Shielding>";
    G4Exception("Xenon1tPhysicsList::Xenon1tPhysicsList()", "PhysicsList",
                FatalException, msg);
  }
   if(HadronInelasticPhysics){
     // pType of Hadron physics is required by ReplacePhysics()
     // As default, it is not set, thus is should be set manually.
     // For future, Geant4 will be updated to fix this bug.
     HadronInelasticPhysics->SetPhysicsType(bHadronInelastic);
     ReplacePhysics(HadronInelasticPhysics);
   }

  G4cout << "Xenon1tPhysicsList::SetHadronicModel(): " << name << G4endl;
}

Xenon1tPhysicsList::~Xenon1tPhysicsList() {
  delete m_pMessenger;
}

void Xenon1tPhysicsList::SetCuts() {
  // special for low energy physics
  G4double lowlimit = 250 * eV;
  G4ProductionCutsTable::GetProductionCutsTable()->SetEnergyRange(lowlimit, 100. * GeV);

  G4cout << "Xenon1tPhysicsList::SetCuts:" << G4endl;
  G4cout << " CutLength gamma: " << GetCutValue("gamma")/mm <<" mm" << G4endl;
  G4cout << " CutLength e-: " << GetCutValue("e-")/mm <<" mm" << G4endl;
  G4cout << " CutLength e+: " << GetCutValue("e+")/mm <<" mm" << G4endl;
  G4cout << " CutLength proton: " << GetCutValue("proton")/mm <<" mm" << G4endl;

  if (VerboseLevel > 0) DumpCutValuesTable();
}