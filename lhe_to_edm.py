import FWCore.ParameterSet.Config as cms
import sys

filein = sys.argv[2]
fileout = sys.argv[3]


process=cms.Process("TEST")
process.source = cms.Source("LHESource",
    #fileNames = cms.untracked.vstring('file:/afs/cern.ch/user/s/seungjun/public/lhe_product/pwgevents-0001.lhe')
    fileNames = cms.untracked.vstring('file:'+filein)
)

#process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(100))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.configurationMetadata = cms.untracked.PSet(
  version = cms.untracked.string('alpha'),
  name = cms.untracked.string('LHEF input'),
  annotation = cms.untracked.string('ttbar')
)

process.LHE = cms.OutputModule("PoolOutputModule",
  dataset = cms.untracked.PSet(dataTier = cms.untracked.string('LHE')),
  fileName = cms.untracked.string(fileout)
)

process.outpath = cms.EndPath(process.LHE)
