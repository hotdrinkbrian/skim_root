import os, sys
import multiprocessing as mp
import copy
import math
from array import array
from ROOT import gROOT, TFile, TTree, TObject, TH1, TH1F, AddressOf
from timeit import default_timer as timer
#start= timer()

# Import objects (structs)
#similar to root[0] bash: .L means load
gROOT.ProcessLine('.L /afs/desy.de/user/h/hezhiyua/private/git1/skim_root/Objects_m1.h+')
#gROOT.ProcessLine('.L /home/brian/skimtest/Objects_m1.h+')
from ROOT import JetType, JetTypeSmall

#args = '/home/brian/skimtest/'
args = '/nfs/dust/cms/user/lbenato/RecoStudies_ntuples_v4/'
args1 = '/afs/desy.de/user/h/hezhiyua/private/skimed_data/'

#adjusted for different oldfile location
#fn = 'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_small.root'

#fn = 'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'
fn = 'VBFH_HToSSTobbbb_MH-125_MS-40_ctauS-500_TuneCUETP8M1_13TeV-powheg-pythia8.root'
path = args
s = path + fn
newFileName = fn.replace('.root','_skimed.root')

#jobs = []
# Struct
Jets1 = JetTypeSmall() #will contain all jets
"""
Jet1o = JetType()
Jet2o = JetType()
Jet3o = JetType()
Jet4o = JetType()
"""

#test dict
num_of_jets = 8
#--------------------------------
Jet_old_dict = {}
for j in range(num_of_jets):  
    Jet_old_dict[j+1] = JetType()
#--------------------------------

#-------------------------------------
cs = {}
cs['pt_L'] = 'pt' + '>' + '15'
cs['eta_L'] = 'eta' + '>' + '-2.4' 
cs['eta_U'] = 'eta' + '<' + '2.4'
#
cs['dR_q1_U'] = 'dR_q1' + '<' + '0.4'
cs['dR_q2_U'] = 'dR_q2' + '<' + '0.4'
cs['dR_q3_U'] = 'dR_q3' + '<' + '0.4'
cs['dR_q4_U'] = 'dR_q4' + '<' + '0.4'
#
cs['dR_q1_L'] = 'dR_q1' + '>' + '0.4'
cs['dR_q2_L'] = 'dR_q2' + '>' + '0.4'
cs['dR_q3_L'] = 'dR_q3' + '>' + '0.4'
cs['dR_q4_L'] = 'dR_q4' + '>' + '0.4'
#-------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------
condition_str_dict = {}
for j in range(num_of_jets):
    prs = 'Jet_old_dict[' +str(j+1) + '].'
    a = ' and '
    o = ' or '
    condition_str_dict[j+1] = '(' + prs + cs['pt_L'] + ')' +\
                              a +\
                              '(' + prs + cs['eta_L'] + a + prs + cs['eta_U'] + ')' +\
                              a +\
                              '(' +\
                              '(' + prs + cs['dR_q1_U'] + a + prs + cs['dR_q2_L'] + a + prs + cs['dR_q3_L'] + a + prs + cs['dR_q4_L'] + ')' +\
                              o +\
                              '(' + prs + cs['dR_q1_L'] + a + prs + cs['dR_q2_U'] + a + prs + cs['dR_q3_L'] + a + prs + cs['dR_q4_L'] + ')' +\
                              o +\
                              '(' + prs + cs['dR_q1_L'] + a + prs + cs['dR_q2_L'] + a + prs + cs['dR_q3_U'] + a + prs + cs['dR_q4_L'] + ')' +\
                              o +\
                              '(' + prs + cs['dR_q1_L'] + a + prs + cs['dR_q2_L'] + a + prs + cs['dR_q3_L'] + a + prs + cs['dR_q4_U'] + ')' +\
                              ')'
    if 'QCD' in fn:
        condition_str_dict[j+1] = '(' + prs + cs['pt_L'] + ')' +\
                                  a +\
                                  '(' + prs + cs['eta_L'] + a + prs + cs['eta_U'] + ')'

print condition_str_dict[1]
#---------------------------------------------------------------------------------------------------------------------------------

"""
#------------------------------------------------------------------------------------------------------
a = ['pt','eta','phi','chf','nhf','phf','elf','muf','chm','cm','nm','dR_q1','dR_q2','dR_q3','dR_q4']
aa =''
for s in a:
    #aa = aa + s+'/f:'
    aa = '        Jets4.'+s+' = Jet4o.'+s
    print aa
#------------------------------------------------------------------------------------------------------
"""

#-----------------------------------------------------------------------------------------------------------
def skim(name):
    print 'filename:', name

    oldFile = TFile(name, "READ")
    oldTree = oldFile.Get("reconstruction/tree") 
    #locate and register the Jet branches of the old ttree
    #oldTree.SetBranchAddress("Jet1", AddressOf(Jet1o, 'pt') ); 
    for j in range(num_of_jets):
        oldTree.SetBranchAddress( 'Jet' + str(j+1) , AddressOf(Jet_old_dict[j+1], 'pt') );

    print 'skimming file',oldFile.GetName(),'\tevents =',oldTree.GetEntries(),'\tweight =',oldTree.GetWeight()

    newFile = TFile('Skim/' + newFileName, "RECREATE")
    newFile.cd()
    newTree = TTree("tree44", "tree44")
    newTree.Branch( 'Jet1s', Jets1, 'pt/F:eta/F:chf/F:nhf/F:phf/F:elf/F:muf/F:chm/I:cm/I:nm/I:dR_q1/F:dR_q2/F:dR_q3/F:dR_q4/F' )
    #newTree.Branch( 'Jet2s', Jets2, 'pt/F:eta/F:chf/F:nhf/F:phf/F:elf/F:muf/F:chm/I:cm/I:nm/I:dR_q1/F:dR_q2/F:dR_q3/F:dR_q4/F' )
    # this attribute list must exactly match (the order of) the features in the header file!!!! 

    ti = 80000
    #theweight = oldTree.GetWeight() 
    for i in range(  0 , oldTree.GetEntries()  ):    # why -1?
        if i ==0:
            start = timer()
        elif i%ti == 2:
            start = timer()

        oldTree.GetEntry(i) 
        # selections
        # Trigger
        """
        if  Jet1o.pt>15 \
            and \
            (Jet1o.eta>-2.4 or Jet1o.eta<2.4) \
            and \
            ( \
            (Jet1o.dR_q1<0.4 and Jet1o.dR_q2>0.4 and Jet1o.dR_q3>0.4 and Jet1o.dR_q4>0.4) \
            or \
            (Jet1o.dR_q2<0.4 and Jet1o.dR_q1>0.4 and Jet1o.dR_q3>0.4 and Jet1o.dR_q4>0.4) \
            or \
            (Jet1o.dR_q3<0.4 and Jet1o.dR_q2>0.4 and Jet1o.dR_q1>0.4 and Jet1o.dR_q4>0.4) \
            or \
            (Jet1o.dR_q4<0.4 and Jet1o.dR_q2>0.4 and Jet1o.dR_q3>0.4 and Jet1o.dR_q1>0.4) \
            ) \
            : 
            # set new leaf values to old ones  
            # this attribute list must exactly match (the order of) the features in the header file!!!!    
            Jets1.pt    = Jet1o.pt
            Jets1.eta   = Jet1o.eta
            Jets1.phi   = Jet1o.phi
            Jets1.chf   = Jet1o.chf
            Jets1.nhf   = Jet1o.nhf
            Jets1.phf   = Jet1o.phf
            Jets1.elf   = Jet1o.elf
            Jets1.muf   = Jet1o.muf     
            Jets1.chm   = Jet1o.chm
            Jets1.cm    = Jet1o.cm
            Jets1.nm    = Jet1o.nm
            Jets1.dR_q1 = Jet1o.dR_q1
            Jets1.dR_q2 = Jet1o.dR_q2
            Jets1.dR_q3 = Jet1o.dR_q3
            Jets1.dR_q4 = Jet1o.dR_q4
            
            newTree.Fill()
        """    
        for j in range(num_of_jets):
            if eval( condition_str_dict[j+1] ):
                Jets1.pt    = Jet_old_dict[j+1].pt
                Jets1.eta   = Jet_old_dict[j+1].eta
                Jets1.phi   = Jet_old_dict[j+1].phi
                Jets1.chf   = Jet_old_dict[j+1].chf
                Jets1.nhf   = Jet_old_dict[j+1].nhf
                Jets1.phf   = Jet_old_dict[j+1].phf
                Jets1.elf   = Jet_old_dict[j+1].elf
                Jets1.muf   = Jet_old_dict[j+1].muf     
                Jets1.chm   = Jet_old_dict[j+1].chm
                Jets1.cm    = Jet_old_dict[j+1].cm
                Jets1.nm    = Jet_old_dict[j+1].nm
                Jets1.dR_q1 = Jet_old_dict[j+1].dR_q1
                Jets1.dR_q2 = Jet_old_dict[j+1].dR_q2
                Jets1.dR_q3 = Jet_old_dict[j+1].dR_q3
                Jets1.dR_q4 = Jet_old_dict[j+1].dR_q4    
                newTree.Fill()

        #########################################################  
        if i%2 == 0:
            ss = '.'
        elif i%2 == 1:
            ss = 'o' 
        if i%ti == 1 and i>ti:
            end = timer() 
            dt = end-start
            tl = int( ((oldTree.GetEntries()-i)/ti ) * dt )
            if tl > 60:
                sys.stdout.write("\r" + 'time left: ' + str( tl/60 ) + 'min' + ss)
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






