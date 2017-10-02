setwd("/Users/kxu/Research/HGG_Chromium/SJHGG019_S-TB-08-1210/Automation/")
list.files()

# convert matrix to pairs (softclip)
H <- read.csv("matrix_softclip.txt", header=F,  sep="\t", stringsAsFactors=FALSE)   
matrix <-H[,-1]
rownames(matrix) <- H[,1]
colnames(matrix) <- H[,1]

matrix["seg_8_R","seg_9_L"]

C1 <- NULL
C2 <- NULL
C3 <- NULL
C4 <- NULL
C5 <- NULL
for(i in 1:59) {
  for(j in (i+1):60) {
    C1 <- c(C1,rownames(matrix)[i])
    C2 <- c(C2,colnames(matrix)[j])
    C3 <- c(C3,matrix[i,j])
    C4 <- c(C4,matrix[j,i])
    total <- matrix[i,j] + matrix[j,i]
    C5 <- c(C5,total)
  }
}
DF <- data.frame(C1,C2,C3,C4,C5)
names(DF) <- c("nodeA", "nodeB", "AtoB", "BtoA", "Total")
DF <- subset(DF, Total > 0)
sortedDF <- DF[order(DF$Total, decreasing = T),]
write.table(sortedDF, "edges_softclip.txt", quote=F, sep="\t", row.names=F, col.names=T)




# convert matrix to pairs (discordant)
H <- read.csv("matrix_discordant.txt", header=T,  sep="\t", stringsAsFactors=FALSE)   
matrix <-H[,-1]
rownames(matrix) <- H[,1]
colnames(matrix) <- H[,1]

matrix["seg_8_R","seg_9_L"]

C1 <- NULL
C2 <- NULL
C3 <- NULL
C4 <- NULL
C5 <- NULL
for(i in 1:59) {
  for(j in (i+1):60) {
    C1 <- c(C1,rownames(matrix)[i])
    C2 <- c(C2,colnames(matrix)[j])
    C3 <- c(C3,matrix[i,j])
    C4 <- c(C4,matrix[j,i])
    total <- matrix[i,j] + matrix[j,i]
    C5 <- c(C5,total)
  }
}
DF <- data.frame(C1,C2,C3,C4,C5)
names(DF) <- c("nodeA", "nodeB", "AtoB", "BtoA", "Total")
DF <- subset(DF, Total > 0)
sortedDF <- DF[order(DF$Total, decreasing = T),]
write.table(sortedDF, "edges_discordant.txt", quote=F, sep="\t", row.names=F, col.names=T)




# convert matrix to pairs (shared discordant)
H <- read.csv("matrix_discordant_sharedhits.txt", header=T,  sep="\t", stringsAsFactors=FALSE)   
matrix <-H[,-1]
rownames(matrix) <- H[,1]
colnames(matrix) <- H[,1]

matrix["seg_8_R","seg_9_L"]

C1 <- NULL
C2 <- NULL
C3 <- NULL
C4 <- NULL
C5 <- NULL
for(i in 1:59) {
  for(j in (i+1):60) {
    C1 <- c(C1,rownames(matrix)[i])
    C2 <- c(C2,colnames(matrix)[j])
    C3 <- c(C3,matrix[i,j])
    C4 <- c(C4,matrix[j,i])
    total <- matrix[i,j] + matrix[j,i]
    C5 <- c(C5,total)
  }
}
DF <- data.frame(C1,C2,C3,C4,C5)
names(DF) <- c("nodeA", "nodeB", "AtoB", "BtoA", "Total")
DF <- subset(DF, Total > 0)
sortedDF <- DF[order(DF$Total, decreasing = T),]
write.table(sortedDF, "edges_shared_discordant.txt", quote=F, sep="\t", row.names=F, col.names=T)




