// Ben Chappell

import java.lang.Math;
import java.security.GeneralSecurityException;

import org.jblas.*;
import java.util.*;
import javax.lang.model.util.ElementScanner6;
import java.io.*;

// Need to make sure that the jblas package is installed.
// Compile with statement javac -cp '.:jblas-1.2.4.jar' SVM.java
// Run with statement java -cp '.:jblas-1.2.4.jar' SVM 

public class SVM
{
    public static void main(String[] args)
    {

    }

    // Requires column vectors x1 and x2, as well as a variable sigma
    public double gaussianKernel(DoubleMatrix x1, DoubleMatrix x2, double sigma)
    {
        x1 = x1.getColumn(0);
        x2 = x2.getColumn(0);

        DoubleMatrix oneMinuxTwo = x1.sub(x2);

        double similarity = Math.exp( ((0- Math.pow(oneMinuxTwo.sum(),2)) / (2*(Math.pow(sigma, 2.0)))));

        return similarity;
    }
}