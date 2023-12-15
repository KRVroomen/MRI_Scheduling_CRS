set.seed(516)                           # Set the seed for the random number generator
nr.sim <- 5000                          # Number of simulations
n <- 237                              # Sample size, we generate a sample of the size of our sample
alpha <- 0.05                         # Nominal level of the test

#We test for the goodness of fit of the Normal distribution to the differences between patients
mu <- mean(time_dif_2$differences)         # Set the sample value of the mean
sd <- sd(time_dif_2$differences)          # Set the sample value of the standard deviation
reject <- rep(0, times = nr.sim)      # Initialise a vector of 0s to store rejections

for (i in 1:nr.sim){                    # Start the simulations
    ## Step 1: Simulate the sample
    X <- rnorm(n, mean = mu,sd=sd)            
    ## Step 2: test for the differences in distribution
test <- ks.test(time_dif_2$differences,X) 
    ## Step 3: Save the outcome of the test
    if (test$p.value<alpha) {reject[i] <- 1}  # Check if the null hypothesis is rejected
    
}
## Step 4: Summarize
ERF <- mean(reject)                 # Empirical rejection frequency

#We test for the goodness of fit of the Gamma distribution to the durations of the scans
mean_int <- mean(data_type2$Duration)         # Set the value of the sample mean
sd_int <- sd(data_type2$Duration)           # Set the value of the sample sd
reject_int <- rep(0, times = nr.sim)      # Initialise a vector of 0s to store rejections

#get the parameters for gamma distribution
shape <- mean_int^2/sd_int^2
rate <- shape/mean_int

for (i in 1:nr.sim){                    # Start the simulations
  ## Step 1: Simulate the  sample
  Y <- rgamma(n, shape = shape,rate=rate)            # Draw X
  ## Step 2: test for the differences in distribution
  test_int <- ks.test(data_type2$Duration,Y)
  ## Step 3: Save the outcome of the test
  if (test_int$p.value<alpha) {reject_int[i] <- 1}  
  
}
## Step 4: Summarize
ERF_int <- mean(reject_int)                 # Empirical rejection frequency

