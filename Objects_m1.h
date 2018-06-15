//modified by brian
#ifndef OBJECTS_H
#define OBJECTS_H

struct JetTypeSmall {
JetTypeSmall(): pt(-1.), eta(-9.), 
/*phi(-9.),*/
chf(-1.), nhf(-1.), phf(-1.), elf(-1.), muf(-1.), chm(-1), cm(-1), nm(-1), dR_q1(1000), dR_q2(1000), dR_q3(1000), dR_q4(1000) {}
    float pt;
    float eta;
    //float phi;
    float chf;
    float nhf;
    float phf;
    float elf;
    float muf; 
    /*
    float chm;
    float cm;
    float nm;
    */
    int chm;
    int cm;
    int nm;
    float dR_q1;
    float dR_q2;
    float dR_q3;
    float dR_q4;
};








struct JetType {
JetType(): pt(-1.), eta(-9.), phi(-9.), mass(-1.), energy(-1.), ptRaw(-1.), ptUnc(-1.), dPhi_met(-1.), dPhi_Jet1(-1.), puId(-1.), CSV(-99.), CSVR(-99.), CSVRUp(-99.), CSVRDown(-99.), CMVA(-99.), CMVAR(-99.), CMVARUp(-99.), CMVARDown(-99.), QGLikelihood(-1.), chf(-1.), nhf(-1.), phf(-1.), elf(-1.), muf(-1.), ptGenJ(-10.), etaGenJ(-4.), phiGenJ(-4.), massGenJ(-10.),ptGen(-10.), etaGen(-4.), phiGen(-4.), massGen(-10.),

/*pdgIdGen(0.),*/
ptLhe(-10.), etaLhe(-4.), phiLhe(-4.), chm(-1), npr(-1), cm(-1), nm(-1), 
flavour(0),
/*partonFlavour(0), hadronFlavour(0),*/ 

mother(0), isLoose(false), isMedium(false), isTight(false), isTightLepVeto(false), isCSVL(false), isCSVM(false), isCSVT(false), isMatched(false), dR_q1(1000), dR_q2(1000), dR_q3(1000), dR_q4(1000), m_q1(false), m_q2(false), m_q3(false), m_q4(false), dR_pi1(1000), dR_pi2(1000), matchBquark(-1), matchLL(-1)

/*, original_jet_index(-1)*/ {}
    float pt;
    float eta;
    float phi;
    float mass;
    float energy;
    float ptRaw;
    float ptUnc;
    float dPhi_met;
    float dPhi_Jet1;
    float puId;
    float CSV;
    float CSVR;
    float CSVRUp;
    float CSVRDown;
    float CMVA;
    float CMVAR;
    float CMVARUp;
    float CMVARDown;
    float QGLikelihood;
    float chf;
    float nhf;
    float phf;
    float elf;
    float muf;
    float ptGenJ; 
    float etaGenJ;
    float phiGenJ;
    float massGenJ;
    float ptGen;
    float etaGen;
    float phiGen;
    float massGen;
    //int pdgIdGen;
    float ptLhe;
    float etaLhe;
    float phiLhe;
    int chm;
    int npr;
    int cm;
    int nm;

    int flavour;
    //int partonFlavour;
    //int hadronFlavour;

    int mother;
    bool isLoose;
    bool isMedium;
    bool isTight;
    bool isTightLepVeto;
    bool isCSVL;
    bool isCSVM;
    bool isCSVT;
    bool isMatched;
    float dR_q1;
    float dR_q2;
    float dR_q3;
    float dR_q4;
    bool m_q1;
    bool m_q2;
    bool m_q3;
    bool m_q4;
    float dR_pi1;
    float dR_pi2;
    int matchBquark;
    int matchLL;
    //int original_jet_index;
};























struct JetTypeSgn {
JetTypeSgn(): pt(-1.), eta(-9.), phi(-9.), mass(-1.), energy(-1.), ptRaw(-1.), ptUnc(-1.), dPhi_met(-1.), dPhi_Jet1(-1.), puId(-1.), CSV(-99.), CSVR(-99.), CSVRUp(-99.), CSVRDown(-99.), CMVA(-99.), CMVAR(-99.), CMVARUp(-99.), CMVARDown(-99.), QGLikelihood(-1.), chf(-1.), nhf(-1.), phf(-1.), elf(-1.), muf(-1.), ptGenJ(-10.), etaGenJ(-4.), phiGenJ(-4.), massGenJ(-10.),ptGen(-10.), etaGen(-4.), phiGen(-4.), massGen(-10.), pdgIdGen(0.), ptLhe(-10.), etaLhe(-4.), phiLhe(-4.), chm(-1), npr(-1), cm(-1), nm(-1), partonFlavour(0), hadronFlavour(0), mother(0), isLoose(false), isMedium(false), isTight(false), isTightLepVeto(false), isCSVL(false), isCSVM(false), isCSVT(false), isMatched(false), dR_q1(1000), dR_q2(1000), dR_q3(1000), dR_q4(1000), m_q1(false), m_q2(false), m_q3(false), m_q4(false), dR_pi1(1000), dR_pi2(1000), matchBquark(-1), matchLL(-1), original_jet_index(-1) {}
    float pt;
    float eta;
    float phi;
    float mass;
    float energy;
    float ptRaw;
    float ptUnc;
    float dPhi_met;
    float dPhi_Jet1;
    float puId;
    float CSV;
    float CSVR;
    float CSVRUp;
    float CSVRDown;
    float CMVA;
    float CMVAR;
    float CMVARUp;
    float CMVARDown;
    float QGLikelihood;
    float chf;
    float nhf;
    float phf;
    float elf;
    float muf;
    float ptGenJ; 
    float etaGenJ;
    float phiGenJ;
    float massGenJ;
    float ptGen;
    float etaGen;
    float phiGen;
    float massGen;
    int pdgIdGen;
    float ptLhe;
    float etaLhe;
    float phiLhe;
    int chm;
    int npr;
    int cm;
    int nm;

    //int flavour;
    int partonFlavour;
    int hadronFlavour;

    int mother;
    bool isLoose;
    bool isMedium;
    bool isTight;
    bool isTightLepVeto;
    bool isCSVL;
    bool isCSVM;
    bool isCSVT;
    bool isMatched;
    float dR_q1;
    float dR_q2;
    float dR_q3;
    float dR_q4;
    bool m_q1;
    bool m_q2;
    bool m_q3;
    bool m_q4;
    float dR_pi1;
    float dR_pi2;
    int matchBquark;
    int matchLL;
    int original_jet_index;
};


#endif
