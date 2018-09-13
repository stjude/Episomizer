#!/usr/bin/env Rscript

# This file is part of Episomizer.
# Author: Ke (Corey) Xu, PhD
# Contact: kxu101@gmail.com


args <- commandArgs(trailingOnly=TRUE)

CNA <- read.csv(args[1], header=F,  sep="\t", stringsAsFactors=FALSE)     # First input: CNA_region_refined.bed  
boundryNum <- dim(CNA)[1] * 2
segName <- c(rbind(paste(CNA$V4,"L",sep=""), paste(CNA$V4,"R",sep="")))


# convert matrix to pairs (softclip)
H <- read.csv(args[2], header=T,  sep="\t", stringsAsFactors=FALSE)       # Second input: matrix_softclip.txt / matrix_discordant.txt / matrix_bridge.txt
matrix <-H[,-1]
rownames(matrix) <- segName
colnames(matrix) <- segName

C1 <- NULL
C2 <- NULL
C3 <- NULL
C4 <- NULL
C5 <- NULL
for(i in 1:(boundryNum-1)) {
  for(j in (i+1):boundryNum) {
    C1 <- c(C1,rownames(matrix)[i])
    C2 <- c(C2,colnames(matrix)[j])
    C3 <- c(C3,matrix[i,j])
    C4 <- c(C4,matrix[j,i])
    total <- matrix[i,j] + matrix[j,i]
    C5 <- c(C5,total)
  }
}
DF <- data.frame(C1, C2, C3, C4, C5)
names(DF) <- c("nodeA", "nodeB", "AtoB", "BtoA", "Total")
DF <- subset(DF, Total > 0)
sortedDF <- DF[order(DF$Total, decreasing = T),]
write.table(sortedDF, args[3], quote=F, sep="\t", row.names=F, col.names=T)   # Output: putative_edges_softclip.txt / putative_edges_discordant.txt / putative_edges_bridge.txt