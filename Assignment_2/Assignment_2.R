setwd("") #Set the Working Directory
retention <- read.table("Retention.txt", sep = "\t", header = TRUE)

#Bell Curves

summary(retention)

spend_den <- density(retention$spend)
plot(spend_den,main="Plot for Spend")

apret_den <- density(retention$apret)
plot(apret_den,main="Plot for Avg Retention Rate")

apret_top10 <- density(retention$top10)
plot(apret_top10,main="Plot for Top 10 % Students")

apret_rejr <- density(retention$rejr)
plot(apret_rejr,main="Plot for Rejection Rate")

apret_tstsc <- density(retention$tstsc)
plot(apret_tstsc,main="Plot for Avg Test Scores")

apret_pacc <- density(retention$pacc)
plot(apret_pacc,main="Plot for % of Admitted Applicants")

apret_strat <- density(retention$strat)
plot(apret_strat,main="Plot for Student Teacher Ratio")

apret_salar <- density(retention$salar)
plot(apret_salar,main="Plot for Average Faculty Salary")


#Histogram Plots

Retention_Rate <- retention$apret
hist(Retention_Rate,main = "Histogram of Avg Retention Rate")


Average_Test_Scores <- retention$tstsc
hist(Average_Test_Scores,main = "Histogram of Avg Test Scores")


Average_Salary <- retention$salar
hist(Average_Salary,main = "Histogram of Avg Faculty Salary")

#Regression Plots

reg_apret_sal <- lm(formula=retention$apret~retention$salar)

plot(retention$salar, retention$apret, xlim=c(min(retention$salar)-5, max(retention$salar)+5), ylim=c(min(retention$apret)-10, max(retention$apret)+10),xlab = "Average Faculty Salary",ylab="Average Retention Rate")
title(main="Regression for apret and salar")
abline(reg_apret_sal, lwd=2)

summary(reg_apret_sal)



reg_apret_tstsc <- lm(formula=retention$apret~retention$tstsc)

plot(retention$tstsc, retention$apret, xlim=c(min(retention$tstsc)-5, max(retention$tstsc)+5), ylim=c(min(retention$apret)-10, max(retention$apret)+10),xlab = "Average Test Scores",ylab="Average Retention Rate")

abline(reg_apret_tstsc, lwd=2)
title(main="Regression for apret and tstsc")
summary(reg_apret_tstsc)



reg_apret_tstsc_salar <- lm(formula=retention$apret~retention$tstsc+retention$salar)

summary(reg_apret_tstsc_salar)
