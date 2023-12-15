library(fitdistrplus)
data <- read.csv('ScanRecords.csv')
data_type1 <- data[data$PatientType=='Type 1',]
data_type2 <- data[data$PatientType=='Type 2',]
#Getting differences for both patients
time_dif_1 <- data.frame(differences = rep(NA, times = 377))
for(i in 2:378){
  if(data_type1$Date[i]==data_type1$Date[i-1]){
    time_dif_1[i-1,1] <- data_type1$Time[i]- data_type1$Time[i-1]
  }
  else{
    time_dif_1[i-1,1] <- 9 + data_type1$Time[i] - data_type1$Time[i-1]
  }
}


#Patient 1 Duration, disribution: Normal
mean(data_type1$Duration)
sd(data_type1$Duration)
summary(rnorm(n=1000,mean=mean(data_type1$Duration),sd=sd(data_type1$Duration)))

#Patient 1 Differences between times disribution: Exponential
mean(time_dif_1$differences)
#lambda:
1/mean(time_dif_1$differences)

#Patient 2 Duration, distribution: Gamma
#remember we use μ=αβ 
mean <- mean(data_type2$Duration)
sd <- sd(data_type2$Duration)
alpha <- mean^2/sd^2
beta <- alpha/mean
hist(rgamma(500,alpha,beta))

#patient 2 intervals
time_dif_2 <- data.frame(differences = rep(NA, times = 237))
for(i in 2:238){
  if(data_type2$Date[i]==data_type2$Date[i-1]){
    time_dif_2[i-1,1] <- data_type2$Time[i]- data_type2$Time[i-1]
  }
  else{
    time_dif_2[i-1,1] <- 9 + data_type2$Time[i] - data_type2$Time[i-1]
  }
}
descdist(time_dif_2$differences, discrete = FALSE,boot = 500)
hist(time_dif_2$differences)


