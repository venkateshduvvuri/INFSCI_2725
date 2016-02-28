
#Setting Working Directory
setwd("C:\\Users\\Venkatesh\\Desktop\\Ass4")

#Reading the csv into a Data Frame
train <- read.csv("train.csv")

#Opon verifying the data, found some rows with N/A values. Removing such rows.
train <- na.omit(train)

#Loading ggplot2 Library
library(ggplot2)

#There are Only 2 levels for Survival. So, Converting them to factors.
survived <- as.factor(train$Survived)

#Plotting Histogram with Age on X-Axis and the Count on Y-Axis
ggplot(train, aes(Age, fill = survived)) +  geom_histogram(alpha = 0.5,colour="blue",position="identity",bins = 40)

#Whisker Plot showing information about survival and age

boxplot(Age~survived,data=train, main="Rate", xlab="Age vs Survival", ylab="Age")

#Facet Grid, Showing Age, Survival and Density in a single plot.

ggplot(train, aes(x=Age)) + geom_histogram(aes(y = ..density..)) + geom_density() +facet_grid(Survived ~ Sex)

#Violin plot Age vs Sex

ggplot(train) + geom_violin(alpha=0.5,aes(x = Sex, y = Age))

#Heatmap

#Had filter on the Age because, the plot was not clear considering all the passengers or putting a filter on any other Factor
#Selecting passengers with Age>50
train1 <- subset(train, Age>50)

#Removing Passenger Id Column. Will use the Passenger Names in the Plot. Will make more sense.
train1 <- train1[,2:12]

#Selecting Passenger Names.
row.names(train1) <- train1$Name

#Converting the Data into Matrix
train_matrix <- data.matrix(train1)

#HeatMap Plot
heatmap(train_matrix,Rowv=NA, Colv=NA, col = heat.colors(15), scale="column", margins=c(5,10))

