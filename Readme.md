# python

Welcome to my test.

Although it can be weird this test is not going to be made in Java and I am going to take advantage to play with python and a different solution. The final result has not been very brillant because it is incomplete, it does not check groups and the code is not very beauty and not vere tested also, but the value of this test is to show how a different solution can be achieved through evolutionary computation.

It is well known how airlines tries to save time in the boarding process, and it is also well known different algorithms to solve it. One of this solutions comes from Genetic Algorithms (GA) that tries to solve in an heuristic manner.

When you develop a GA you have to take into account the following:
1. INITIAL POPULATION
    How many chromosomes you are going to deal with
2. FITNESS FUNCTION
    How to measure how well the solution of each gen is
3. SELECTION
    The best genes pass to the next generation
4. CROSSOVER
    Mix the genes between chromosomes
5. MUTATION
    Randomly a genes can mutate
6. ITERATE OVER THE NEW POPULATION
    Iterate following the process above

So we start with a population of two chromosomes and iterate searching the best satisfaction return taking into account the restrictions. Each chromosome has genes that are different aircraft configurations


HOW TO RUN
To execute this you need to install docker and run the following in the terminal

docker build -t boarding_test -rm .
docker run boarding_test

TEST

Test can be achieved modifiying initial input.txt file
