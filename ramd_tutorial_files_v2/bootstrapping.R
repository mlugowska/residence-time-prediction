
#------------------- READ RAMD DATA
getdata <- function(name) {
	s <- read.table(name,header = FALSE)
	x1 <- s[["V2"]]
     return (x1/500000.0)
}


#---------------------- GET RAMD effective dissociation TIME from RAMD data
gettime <- function(xtot) {
      htot_norm <- sort(xtot, decreasing = TRUE)
      k<- 1
      for (i in seq_along(htot_norm)) {
           if (k > length (htot_norm)/2.0) break
           k <- k+1
      }
      restime <- (htot_norm[k-1]+htot_norm[k+1])/2.0
      return (restime)
}

#-------------------- BOOTSTRAPPING DATA
getbootstr  <- function(x) {
    data <- gettime(x)
    for (i in 1:10000) {
            y <-sample(x, length(x)*0.8,replace=T)
    		data <- c(data,gettime(y))
    }
    return (data)
}





filelist <- list.files(path=".",pattern=paste("times","_",sep=""),full.names = TRUE)
out <- "FILE to be analyzed:"
out
filelist
list_out <- NULL
 for (k in seq_along(filelist)) {
    data_inp <- getdata(filelist[k])
    x1=getbootstr(data_inp)
    out_distr=paste(MEAN=c(mean(x1),SD=sd(x1)))
    list_out <- c(list_out,mean(x1),sd(x1))
    h <- hist(x1)
    write(paste(h$breaks,h$density),paste("distribution.dat", toString(k),sep=""),ncolumns = 1, sep = "\t")
}
out <- " MEAN /ns   SD "
out
list_out


