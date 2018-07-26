import os, sys
import multiprocessing as mp
import copy
import math
from array import array
from ROOT import gROOT, TFile, TTree, TObject, TH1, TH1F, AddressOf
from timeit import default_timer as timer
# Import objects (structs)
#similar to root[0] bash: .L means load
gROOT.ProcessLine('.L /home/brian/datas/pfc_test/temp/llp_test/skim/Objects_m1.h+')
from ROOT import JetType, JetTypeSmall, JetTypeSgn, JetTypePFC_fourVect    #, JetTypePFCSmall

args  = '/home/brian/datas/pfc_test/temp/llp_test/'
args1 = '/home/brian/datas/pfc_test/temp/llp_test/'
#args  = '/home/brian/datas/pfc_test/output/'
#args1 = '/home/brian/datas/pfc_test/output/'
#args  = '/beegfs/desy/user/hezhiyua/pfc_test/raw_data/'
#args1 = '/beegfs/desy/user/hezhiyua/pfc_test/raw_data/'

#adjusted for different oldfile location
fn = ''
path = args
s = fn
newFileName = fn.replace('.root','_skimed.root')

#jobs = []

lola_on = 0 # 1: prepared for lola
NJT = 2 #branch using a structure with less features:1
ct_dep = 0 #1 for ct dependence comparison
cut_on = 1
#life_time = ['0','0p1','0p05','1','5','10','25','50','100','500','1000','2000','5000','10000']
life_time = ['500']
len_of_lt = len(life_time)

if   ct_dep == 0:
    channel = {'QCD':'QCD_HT50To100_pfc.root'}
elif ct_dep == 1:
    channel = {}
    for lt in life_time:
        channel['ct' + lt] = 'VBFH_HToSSTobbbb_MH-125_MS-40_ctauS-' + lt + '_pfc_t1.root'
        #channel['ct' + lt] = 'VBFH_HToSSTobbbb_MH-125_MS-40_ctauS-' + lt + '_TuneCUETP8M1_13TeV-powheg-pythia8.root'

#test dict
num_of_jets = 1 #4

# Struct
if   lola_on == 0:
    Jets1 = JetTypeSmall()#JetTypePFC_fourVect()#JetTypeSmall() #for bdt: JetTypeSmall; for lola: JetTypePFC_fourVect
elif lola_on == 1:
    Jets1 = JetTypePFC_fourVect()

#-------------------------------------
cs = {}
cs['pt_L'] = 'pt' + '>' + '15'
cs['eta_L'] = 'eta' + '>' + '-2.4' 
cs['eta_U'] = 'eta' + '<' + '2.4'
#-------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------
condition_str_dict = {}
for j in range(num_of_jets):
    prs = 'Jet_old_dict[' +str(j+1) + '].'
    a = ' and '
    o = ' or '
    condition_str_dict[j+1] = '(' + prs + cs['pt_L'] + ')' +\
                              a +\
                              '(' + prs + cs['eta_L'] + ')' +\
                              a +\
                              '(' + prs + cs['eta_U'] + ')'

if   cut_on == 1:
    print condition_str_dict[1]
elif cut_on == 0:
    print 'no cut applied~'
#---------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
def skim_c( name , newFileName ):
    #--------------------------------
    Jet_old_dict = {}
    for j in range(num_of_jets):
        if   NJT == 1:
            Jet_old_dict[j+1] = JetTypeSgn()
        elif NJT == 2:
            Jet_old_dict[j+1] = JetType()
    #--------------------------------

    print 'filename:', name

    oldFile = TFile(name, "READ")
    oldTree = oldFile.Get("ntuple/tree") # "reconstruction/tree"
    #locate and register the Jet branches of the old ttree 
    for j in range(num_of_jets):
        if 'QCD' in name:
            oldTree.SetBranchAddress( 'CHSJet' + str(j+1) , AddressOf(Jet_old_dict[j+1], 'pt') ); #'Jet'
        elif 'ctauS' in name:
            oldTree.SetBranchAddress( 'MatchedCHSJet' + str(j+1) , AddressOf(Jet_old_dict[j+1], 'pt') ); #'MatchedJet'

    print 'skimming file',oldFile.GetName(),'\tevents =',oldTree.GetEntries(),'\tweight =',oldTree.GetWeight()

    newFile = TFile('Skim/' + newFileName, "RECREATE")
    newFile.cd()
    newTree = TTree("tree44", "tree44")

    if   lola_on == 0:
        newTree.Branch( 'Jet1s', Jets1, 'pt/F:eta/F:mass/F:chf/F:nhf/F:phf/F:elf/F:muf/F:chm/I:cm/I:nm/I' )
    elif lola_on == 1:
        newTree.Branch( 'Jet1s', Jets1, 'pfc1_energy/F:pfc1_px/F:pfc1_py/F:pfc1_pz/F:pfc2_energy/F:pfc2_px/F:pfc2_py/F:pfc2_pz/F:pfc3_energy/F:pfc3_px/F:pfc3_py/F:pfc3_pz/F:pfc4_energy/F:pfc4_px/F:pfc4_py/F:pfc4_pz/F:pfc5_energy/F:pfc5_px/F:pfc5_py/F:pfc5_pz/F:pfc6_energy/F:pfc6_px/F:pfc6_py/F:pfc6_pz/F:pfc7_energy/F:pfc7_px/F:pfc7_py/F:pfc7_pz/F:pfc8_energy/F:pfc8_px/F:pfc8_py/F:pfc8_pz/F:pfc9_energy/F:pfc9_px/F:pfc9_py/F:pfc9_pz/F:pfc10_energy/F:pfc10_px/F:pfc10_py/F:pfc10_pz/F:pfc11_energy/F:pfc11_px/F:pfc11_py/F:pfc11_pz/F:pfc12_energy/F:pfc12_px/F:pfc12_py/F:pfc12_pz/F:pfc13_energy/F:pfc13_px/F:pfc13_py/F:pfc13_pz/F:pfc14_energy/F:pfc14_px/F:pfc14_py/F:pfc14_pz/F:pfc15_energy/F:pfc15_px/F:pfc15_py/F:pfc15_pz/F:pfc16_energy/F:pfc16_px/F:pfc16_py/F:pfc16_pz/F:pfc17_energy/F:pfc17_px/F:pfc17_py/F:pfc17_pz/F:pfc18_energy/F:pfc18_px/F:pfc18_py/F:pfc18_pz/F:pfc19_energy/F:pfc19_px/F:pfc19_py/F:pfc19_pz/F:pfc20_energy/F:pfc20_px/F:pfc20_py/F:pfc20_pz/F:pfc21_energy/F:pfc21_px/F:pfc21_py/F:pfc21_pz/F:pfc22_energy/F:pfc22_px/F:pfc22_py/F:pfc22_pz/F:pfc23_energy/F:pfc23_px/F:pfc23_py/F:pfc23_pz/F:pfc24_energy/F:pfc24_px/F:pfc24_py/F:pfc24_pz/F:pfc25_energy/F:pfc25_px/F:pfc25_py/F:pfc25_pz/F:pfc26_energy/F:pfc26_px/F:pfc26_py/F:pfc26_pz/F:pfc27_energy/F:pfc27_px/F:pfc27_py/F:pfc27_pz/F:pfc28_energy/F:pfc28_px/F:pfc28_py/F:pfc28_pz/F:pfc29_energy/F:pfc29_px/F:pfc29_py/F:pfc29_pz/F:pfc30_energy/F:pfc30_px/F:pfc30_py/F:pfc30_pz/F:pfc31_energy/F:pfc31_px/F:pfc31_py/F:pfc31_pz/F:pfc32_energy/F:pfc32_px/F:pfc32_py/F:pfc32_pz/F:pfc33_energy/F:pfc33_px/F:pfc33_py/F:pfc33_pz/F:pfc34_energy/F:pfc34_px/F:pfc34_py/F:pfc34_pz/F:pfc35_energy/F:pfc35_px/F:pfc35_py/F:pfc35_pz/F:pfc36_energy/F:pfc36_px/F:pfc36_py/F:pfc36_pz/F:pfc37_energy/F:pfc37_px/F:pfc37_py/F:pfc37_pz/F:pfc38_energy/F:pfc38_px/F:pfc38_py/F:pfc38_pz/F:pfc39_energy/F:pfc39_px/F:pfc39_py/F:pfc39_pz/F:pfc40_energy/F:pfc40_px/F:pfc40_py/F:pfc40_pz/F' )
    # this attribute list must exactly match (the order of) the features in the header file!!!! 

    ti = 80000
    #theweight = oldTree.GetWeight() 
    for i in range(  0 , oldTree.GetEntries()  ):    
        if      i == 0:
            start = timer()
        elif i%ti == 2:
            start = timer()

        oldTree.GetEntry(i) 
        # selections
        # Trigger
        
        for j in range(num_of_jets):
            if cut_on == 0:
                condition_str_dict[j+1] = '1'
 
            if eval( condition_str_dict[j+1] ):
                
                if lola_on == 0:
                    Jets1.pt    = Jet_old_dict[j+1].pt
                    Jets1.eta   = Jet_old_dict[j+1].eta
                    Jets1.mass  = Jet_old_dict[j+1].mass
                    Jets1.chf   = Jet_old_dict[j+1].chf
                    Jets1.nhf   = Jet_old_dict[j+1].nhf
                    Jets1.phf   = Jet_old_dict[j+1].phf
                    Jets1.elf   = Jet_old_dict[j+1].elf
                    Jets1.muf   = Jet_old_dict[j+1].muf     
                    Jets1.chm   = Jet_old_dict[j+1].chm
                    Jets1.cm    = Jet_old_dict[j+1].cm
                    Jets1.nm    = Jet_old_dict[j+1].nm
                elif lola_on == 1:
                    Jets1.pfc1_energy    = Jet_old_dict[j+1].pfc1_energy
                    Jets1.pfc1_px        = Jet_old_dict[j+1].pfc1_px
                    Jets1.pfc1_py        = Jet_old_dict[j+1].pfc1_py
                    Jets1.pfc1_pz        = Jet_old_dict[j+1].pfc1_pz
                    Jets1.pfc2_energy    = Jet_old_dict[j+1].pfc2_energy
                    Jets1.pfc2_px        = Jet_old_dict[j+1].pfc2_px
                    Jets1.pfc2_py        = Jet_old_dict[j+1].pfc2_py
                    Jets1.pfc2_pz        = Jet_old_dict[j+1].pfc2_pz
                    Jets1.pfc3_energy    = Jet_old_dict[j+1].pfc3_energy
                    Jets1.pfc3_px        = Jet_old_dict[j+1].pfc3_px
                    Jets1.pfc3_py        = Jet_old_dict[j+1].pfc3_py
                    Jets1.pfc3_pz        = Jet_old_dict[j+1].pfc3_pz
                    Jets1.pfc4_energy    = Jet_old_dict[j+1].pfc4_energy
                    Jets1.pfc4_px        = Jet_old_dict[j+1].pfc4_px
                    Jets1.pfc4_py        = Jet_old_dict[j+1].pfc4_py
                    Jets1.pfc4_pz        = Jet_old_dict[j+1].pfc4_pz
                    Jets1.pfc5_energy    = Jet_old_dict[j+1].pfc5_energy
                    Jets1.pfc5_px        = Jet_old_dict[j+1].pfc5_px
                    Jets1.pfc5_py        = Jet_old_dict[j+1].pfc5_py
                    Jets1.pfc5_pz        = Jet_old_dict[j+1].pfc5_pz
                    Jets1.pfc6_energy    = Jet_old_dict[j+1].pfc6_energy
                    Jets1.pfc6_px        = Jet_old_dict[j+1].pfc6_px
                    Jets1.pfc6_py        = Jet_old_dict[j+1].pfc6_py
                    Jets1.pfc6_pz        = Jet_old_dict[j+1].pfc6_pz
                    Jets1.pfc7_energy    = Jet_old_dict[j+1].pfc7_energy
                    Jets1.pfc7_px        = Jet_old_dict[j+1].pfc7_px
                    Jets1.pfc7_py        = Jet_old_dict[j+1].pfc7_py
                    Jets1.pfc7_pz        = Jet_old_dict[j+1].pfc7_pz
                    Jets1.pfc8_energy    = Jet_old_dict[j+1].pfc8_energy
                    Jets1.pfc8_px        = Jet_old_dict[j+1].pfc8_px
                    Jets1.pfc8_py        = Jet_old_dict[j+1].pfc8_py
                    Jets1.pfc8_pz        = Jet_old_dict[j+1].pfc8_pz
                    Jets1.pfc9_energy    = Jet_old_dict[j+1].pfc9_energy
                    Jets1.pfc9_px        = Jet_old_dict[j+1].pfc9_px
                    Jets1.pfc9_py        = Jet_old_dict[j+1].pfc9_py
                    Jets1.pfc9_pz        = Jet_old_dict[j+1].pfc9_pz
                    Jets1.pfc10_energy    = Jet_old_dict[j+1].pfc10_energy
                    Jets1.pfc10_px        = Jet_old_dict[j+1].pfc10_px
                    Jets1.pfc10_py        = Jet_old_dict[j+1].pfc10_py
                    Jets1.pfc10_pz        = Jet_old_dict[j+1].pfc10_pz
                    Jets1.pfc11_energy    = Jet_old_dict[j+1].pfc11_energy
                    Jets1.pfc11_px        = Jet_old_dict[j+1].pfc11_px
                    Jets1.pfc11_py        = Jet_old_dict[j+1].pfc11_py
                    Jets1.pfc11_pz        = Jet_old_dict[j+1].pfc11_pz
                    Jets1.pfc12_energy    = Jet_old_dict[j+1].pfc12_energy
                    Jets1.pfc12_px        = Jet_old_dict[j+1].pfc12_px
                    Jets1.pfc12_py        = Jet_old_dict[j+1].pfc12_py
                    Jets1.pfc12_pz        = Jet_old_dict[j+1].pfc12_pz
                    Jets1.pfc13_energy    = Jet_old_dict[j+1].pfc13_energy
                    Jets1.pfc13_px        = Jet_old_dict[j+1].pfc13_px
                    Jets1.pfc13_py        = Jet_old_dict[j+1].pfc13_py
                    Jets1.pfc13_pz        = Jet_old_dict[j+1].pfc13_pz
                    Jets1.pfc14_energy    = Jet_old_dict[j+1].pfc14_energy
                    Jets1.pfc14_px        = Jet_old_dict[j+1].pfc14_px
                    Jets1.pfc14_py        = Jet_old_dict[j+1].pfc14_py
                    Jets1.pfc14_pz        = Jet_old_dict[j+1].pfc14_pz
                    Jets1.pfc15_energy    = Jet_old_dict[j+1].pfc15_energy
                    Jets1.pfc15_px        = Jet_old_dict[j+1].pfc15_px
                    Jets1.pfc15_py        = Jet_old_dict[j+1].pfc15_py
                    Jets1.pfc15_pz        = Jet_old_dict[j+1].pfc15_pz
                    Jets1.pfc16_energy    = Jet_old_dict[j+1].pfc16_energy
                    Jets1.pfc16_px        = Jet_old_dict[j+1].pfc16_px
                    Jets1.pfc16_py        = Jet_old_dict[j+1].pfc16_py
                    Jets1.pfc16_pz        = Jet_old_dict[j+1].pfc16_pz
                    Jets1.pfc17_energy    = Jet_old_dict[j+1].pfc17_energy
                    Jets1.pfc17_px        = Jet_old_dict[j+1].pfc17_px
                    Jets1.pfc17_py        = Jet_old_dict[j+1].pfc17_py
                    Jets1.pfc17_pz        = Jet_old_dict[j+1].pfc17_pz
                    Jets1.pfc18_energy    = Jet_old_dict[j+1].pfc18_energy
                    Jets1.pfc18_px        = Jet_old_dict[j+1].pfc18_px
                    Jets1.pfc18_py        = Jet_old_dict[j+1].pfc18_py
                    Jets1.pfc18_pz        = Jet_old_dict[j+1].pfc18_pz
                    Jets1.pfc19_energy    = Jet_old_dict[j+1].pfc19_energy
                    Jets1.pfc19_px        = Jet_old_dict[j+1].pfc19_px
                    Jets1.pfc19_py        = Jet_old_dict[j+1].pfc19_py
                    Jets1.pfc19_pz        = Jet_old_dict[j+1].pfc19_pz
                    Jets1.pfc20_energy    = Jet_old_dict[j+1].pfc20_energy
                    Jets1.pfc20_px        = Jet_old_dict[j+1].pfc20_px
                    Jets1.pfc20_py        = Jet_old_dict[j+1].pfc20_py
                    Jets1.pfc20_pz        = Jet_old_dict[j+1].pfc20_pz
                    Jets1.pfc21_energy    = Jet_old_dict[j+1].pfc21_energy
                    Jets1.pfc21_px        = Jet_old_dict[j+1].pfc21_px
                    Jets1.pfc21_py        = Jet_old_dict[j+1].pfc21_py
                    Jets1.pfc21_pz        = Jet_old_dict[j+1].pfc21_pz
                    Jets1.pfc22_energy    = Jet_old_dict[j+1].pfc22_energy
                    Jets1.pfc22_px        = Jet_old_dict[j+1].pfc22_px
                    Jets1.pfc22_py        = Jet_old_dict[j+1].pfc22_py
                    Jets1.pfc22_pz        = Jet_old_dict[j+1].pfc22_pz
                    Jets1.pfc23_energy    = Jet_old_dict[j+1].pfc23_energy
                    Jets1.pfc23_px        = Jet_old_dict[j+1].pfc23_px
                    Jets1.pfc23_py        = Jet_old_dict[j+1].pfc23_py
                    Jets1.pfc23_pz        = Jet_old_dict[j+1].pfc23_pz
                    Jets1.pfc24_energy    = Jet_old_dict[j+1].pfc24_energy
                    Jets1.pfc24_px        = Jet_old_dict[j+1].pfc24_px
                    Jets1.pfc24_py        = Jet_old_dict[j+1].pfc24_py
                    Jets1.pfc24_pz        = Jet_old_dict[j+1].pfc24_pz
                    Jets1.pfc25_energy    = Jet_old_dict[j+1].pfc25_energy
                    Jets1.pfc25_px        = Jet_old_dict[j+1].pfc25_px
                    Jets1.pfc25_py        = Jet_old_dict[j+1].pfc25_py
                    Jets1.pfc25_pz        = Jet_old_dict[j+1].pfc25_pz
                    Jets1.pfc26_energy    = Jet_old_dict[j+1].pfc26_energy
                    Jets1.pfc26_px        = Jet_old_dict[j+1].pfc26_px
                    Jets1.pfc26_py        = Jet_old_dict[j+1].pfc26_py
                    Jets1.pfc26_pz        = Jet_old_dict[j+1].pfc26_pz
                    Jets1.pfc27_energy    = Jet_old_dict[j+1].pfc27_energy
                    Jets1.pfc27_px        = Jet_old_dict[j+1].pfc27_px
                    Jets1.pfc27_py        = Jet_old_dict[j+1].pfc27_py
                    Jets1.pfc27_pz        = Jet_old_dict[j+1].pfc27_pz
                    Jets1.pfc28_energy    = Jet_old_dict[j+1].pfc28_energy
                    Jets1.pfc28_px        = Jet_old_dict[j+1].pfc28_px
                    Jets1.pfc28_py        = Jet_old_dict[j+1].pfc28_py
                    Jets1.pfc28_pz        = Jet_old_dict[j+1].pfc28_pz
                    Jets1.pfc29_energy    = Jet_old_dict[j+1].pfc29_energy
                    Jets1.pfc29_px        = Jet_old_dict[j+1].pfc29_px
                    Jets1.pfc29_py        = Jet_old_dict[j+1].pfc29_py
                    Jets1.pfc29_pz        = Jet_old_dict[j+1].pfc29_pz
                    Jets1.pfc30_energy    = Jet_old_dict[j+1].pfc30_energy
                    Jets1.pfc30_px        = Jet_old_dict[j+1].pfc30_px
                    Jets1.pfc30_py        = Jet_old_dict[j+1].pfc30_py
                    Jets1.pfc30_pz        = Jet_old_dict[j+1].pfc30_pz
                    Jets1.pfc31_energy    = Jet_old_dict[j+1].pfc31_energy
                    Jets1.pfc31_px        = Jet_old_dict[j+1].pfc31_px
                    Jets1.pfc31_py        = Jet_old_dict[j+1].pfc31_py
                    Jets1.pfc31_pz        = Jet_old_dict[j+1].pfc31_pz
                    Jets1.pfc32_energy    = Jet_old_dict[j+1].pfc32_energy
                    Jets1.pfc32_px        = Jet_old_dict[j+1].pfc32_px
                    Jets1.pfc32_py        = Jet_old_dict[j+1].pfc32_py
                    Jets1.pfc32_pz        = Jet_old_dict[j+1].pfc32_pz
                    Jets1.pfc33_energy    = Jet_old_dict[j+1].pfc33_energy
                    Jets1.pfc33_px        = Jet_old_dict[j+1].pfc33_px
                    Jets1.pfc33_py        = Jet_old_dict[j+1].pfc33_py
                    Jets1.pfc33_pz        = Jet_old_dict[j+1].pfc33_pz
                    Jets1.pfc34_energy    = Jet_old_dict[j+1].pfc34_energy
                    Jets1.pfc34_px        = Jet_old_dict[j+1].pfc34_px
                    Jets1.pfc34_py        = Jet_old_dict[j+1].pfc34_py
                    Jets1.pfc34_pz        = Jet_old_dict[j+1].pfc34_pz
                    Jets1.pfc35_energy    = Jet_old_dict[j+1].pfc35_energy
                    Jets1.pfc35_px        = Jet_old_dict[j+1].pfc35_px
                    Jets1.pfc35_py        = Jet_old_dict[j+1].pfc35_py
                    Jets1.pfc35_pz        = Jet_old_dict[j+1].pfc35_pz
                    Jets1.pfc36_energy    = Jet_old_dict[j+1].pfc36_energy
                    Jets1.pfc36_px        = Jet_old_dict[j+1].pfc36_px
                    Jets1.pfc36_py        = Jet_old_dict[j+1].pfc36_py
                    Jets1.pfc36_pz        = Jet_old_dict[j+1].pfc36_pz
                    Jets1.pfc37_energy    = Jet_old_dict[j+1].pfc37_energy
                    Jets1.pfc37_px        = Jet_old_dict[j+1].pfc37_px
                    Jets1.pfc37_py        = Jet_old_dict[j+1].pfc37_py
                    Jets1.pfc37_pz        = Jet_old_dict[j+1].pfc37_pz
                    Jets1.pfc38_energy    = Jet_old_dict[j+1].pfc38_energy
                    Jets1.pfc38_px        = Jet_old_dict[j+1].pfc38_px
                    Jets1.pfc38_py        = Jet_old_dict[j+1].pfc38_py
                    Jets1.pfc38_pz        = Jet_old_dict[j+1].pfc38_pz
                    Jets1.pfc39_energy    = Jet_old_dict[j+1].pfc39_energy
                    Jets1.pfc39_px        = Jet_old_dict[j+1].pfc39_px
                    Jets1.pfc39_py        = Jet_old_dict[j+1].pfc39_py
                    Jets1.pfc39_pz        = Jet_old_dict[j+1].pfc39_pz
                    Jets1.pfc40_energy    = Jet_old_dict[j+1].pfc40_energy
                    Jets1.pfc40_px        = Jet_old_dict[j+1].pfc40_px
                    Jets1.pfc40_py        = Jet_old_dict[j+1].pfc40_py
                    Jets1.pfc40_pz        = Jet_old_dict[j+1].pfc40_pz


                newTree.Fill()

        #########################################################  
        if i%ti == 1 and i>ti:
            end = timer() 
            dt = end-start
            tl = int( ((oldTree.GetEntries()-i)/ti ) * dt )
            if tl > 60:
                sys.stdout.write("\r" + 'time left: ' + str( tl/60 ) + 'min' )
                sys.stdout.flush()
            else: 
                sys.stdout.write("\r" + 'time left: ' + str( tl/60 ) + 's')
                sys.stdout.flush() 
        #########################################################

    print 'produced skimmed file',newFile.GetName(),'\tevents =',newTree.GetEntries(),'\tweight =',newTree.GetWeight()
    newFile.cd()
    newFile.Write()
    newFile.Close() 
    oldFile.Close()
#-----------------------------------------------------------------------------------------------------------

#-----------===============================
def skim(names): 
    for cc in channel:
        if 'QCD' in channel[cc]:
            nFn = channel[cc].replace('.root','_' + str(num_of_jets) + 'j_skimed.root')
        elif 'ctauS' in channel[cc]:
            nFn = channel[cc].replace('.root','_' + str(num_of_jets) + 'j_skimed.root') #('.root','_4mj_skimed.root')
        ss = path + channel[cc]    
        skim_c(ss,nFn)
#-----------===============================

#=====================================================================================================
os.chdir(args1)
if not os.path.isdir('Skim'): os.mkdir('Skim')

p = mp.Process(target=skim, args=(s,))
p.start()
#=====================================================================================================



"""
#=====================================================================================================
subfiles = [i for i in os.listdir(args) if os.path.isfile(os.path.join(args, i)) and '.root' in i] 
os.chdir(args)
if not os.path.isdir('Skim'): os.mkdir('Skim')

for s in subfiles:
    p = mp.Process(target=skim, args=(s,))
    #jobs.append(p)                              
    p.start()
#=====================================================================================================
"""