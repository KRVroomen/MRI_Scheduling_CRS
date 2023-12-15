set.seed(515)    # Set the seed for the random number generator
B <- 499         # Number of bootstrap replications
alpha <- 0.05    # Nominal level of the test

# I load the differences between times for patients type 2
X <- time_dif_2$differences

n <- length(X)                                          # Sample size
X.bar <- mean(X)                                        # Sample mean of X
St.Dev <- sd(X)                                         # Standard deviation of X

X.bar.star <- rep(NA, times = B)    
St.Dev.star <- rep(NA, times = B)   
for (b in 1:B) {
    J <- sample.int(n, size = n, replace = TRUE)        # Draw the indices J
    X.star <- X[J]                                      # Draw the bootstrap sample
    X.bar.star[b] <- mean(X.star)                          # Bootstrap sample mean
    St.Dev.star[b] <- sd(X.star)                           # Bootstrap standard deviation
}
                          
# Confidence interval for the sample mean
mean_ci <- quantile(X.bar.star, c(alpha / 2, 1 - alpha / 2))
# Confidence interval for the sample variance
variance_ci <- quantile(St.Dev.star, c(alpha / 2, 1 - alpha / 2))
# Convert to minutes 
mean_ci_X_minutes <- mean_ci*60
variance_ci_X_minutes <- variance_ci *60
mean_X_minutes <- X.bar*60
St.Dev_X_minutes <-  St.Dev*60
#######################################################

# I load the duration  for patients type 2
Y <- data_type2$Duration

n_Y <- length(Y)                                          # Sample size
Y.bar <- mean(Y)                                        # Sample mean of Y
St.Dev_Y <- sd(Y)                                         # Standard deviation of Y

Y.bar.star <- rep(NA, times = B)    
St.Dev.star_Y <- rep(NA, times = B)   
for (b in 1:B) {
  J <- sample.int(n_Y, size = n_Y, replace = TRUE)        # Draw the indices J
  Y.star <- Y[J]                                      # Draw the bootstrap sample
  Y.bar.star[b] <- mean(Y.star)                          # Bootstrap sample mean
  St.Dev.star_Y[b] <- sd(Y.star)                           # Bootstrap standard deviation
}

# Confidence interval for the sample mean
mean_ci_Y <- quantile(Y.bar.star, c(alpha / 2, 1 - alpha / 2))
# Confidence interval for the sample variance
variance_ci_Y <- quantile(St.Dev.star_Y, c(alpha / 2, 1 - alpha / 2))
# Convert to minutes 
mean_ci_Y_minutes <- mean_ci_Y*60
variance_ci_Y_minutes <- variance_ci_Y *60
mean_Y_minutes <- Y.bar*60
St.Dev_Y_minutes <-  St.Dev_Y*60
#######################################################

# I load the duration for patients type 1
Z <- data_type1$Duration

n_Z <- length(Z)                                          # Sample size
Z.bar <- mean(Z)                                        # Sample mean of Z
St.Dev_Z <- sd(Z)                                         # Standard deviation of Z

Z.bar.star <- rep(NA, times = B)    
St.Dev.star_Z <- rep(NA, times = B)   
for (b in 1:B) {
  J <- sample.int(n_Z, size = n_Z, replace = TRUE)        # Draw the indices J
  Z.star <- Z[J]                                      # Draw the bootstrap sample
  Z.bar.star[b] <- mean(Z.star)                          # Bootstrap sample mean
  St.Dev.star_Z[b] <- sd(Z.star)                           # Bootstrap standard deviation
}

# Confidence interval for the sample mean
mean_ci_Z <- quantile(Z.bar.star, c(alpha / 2, 1 - alpha / 2))
# Confidence interval for the sample variance
variance_ci_Z <- quantile(St.Dev.star_Z, c(alpha / 2, 1 - alpha / 2))
# Convert to minutes 
mean_ci_Z_minutes <- mean_ci_Z*60
variance_ci_Z_minutes <- variance_ci_Z *60
mean_Z_minutes <- Z.bar*60
St.Dev_Z_minutes <-  St.Dev_Z*60
#######################################################

# I load the differences between times for patients type 1
K <- time_dif_1$differences

n_K <- length(K)                                          # Sample size
K.bar <- mean(K)                                        # Sample mean of K
St.Dev_K <- sd(K)                                         # Standard deviation of K

K.bar.star <- rep(NA, times = B)    
St.Dev.star_K <- rep(NA, times = B)   
for (b in 1:B) {
  J <- sample.int(n_K, size = n_K, replace = TRUE)        # Draw the indices J
  K.star <- K[J]                                      # Draw the bootstrap sample
  K.bar.star[b] <- mean(K.star)                          # Bootstrap sample mean
  St.Dev.star_K[b] <- sd(K.star)                           # Bootstrap standard deviation
}

# Confidence interval for the sample mean
mean_ci_K <- quantile(K.bar.star, c(alpha / 2, 1 - alpha / 2))
# Confidence interval for the sample variance
variance_ci_K <- quantile(St.Dev.star_K, c(alpha / 2, 1 - alpha / 2))
# Convert to minutes 
mean_ci_K_minutes <- mean_ci_K*60
variance_ci_K_minutes <- variance_ci_K *60
mean_K_minutes <- K.bar*60
St.Dev_K_minutes <-  St.Dev_K*60

