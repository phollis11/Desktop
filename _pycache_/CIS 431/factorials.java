import java.math.BigInteger;

public class factorials {
    
    //factorial with loop and long int
    public static long factorial_loop(int num) {
        long sum = num;
        while (num > 1) {
            sum = sum * (num - 1);
            num -= 1;
        }
        return sum;
    }
    //factorial with recursion and long int

    public static long factorial_recurse(int num) {
        if (num == 0) {
            return 1;
        } else {
            return num * factorial_recurse(num - 1);
        }
    }

    //factorial with loop and BigInt
    public static BigInteger BigInt_loop(int num) {
        BigInteger result = BigInteger.ONE;
        for (int i = 2; i <= num; i++) {
            result = result.multiply(BigInteger.valueOf(i));
        }
        return result;
    }

        //factorial with recursion and BigInt
     public static BigInteger BigInt_recurse(int num) {
        if (num == 0) {
            return BigInteger.ONE;
        } else {
            return BigInteger.valueOf(num).multiply(BigInt_recurse(num - 1));
        }
    }

    public static void main(String[] args) {
        //different factorials to calculate
        int n1 = 15;
        int n2 = 25;
        int n3 = 50;
        int n4 = 100;


        // Timing using loop and 15!
        long startLoop = System.nanoTime();
        long resultLoop = factorial_loop(n1);
        long endLoop = System.nanoTime();
        System.out.println("Loop factorial(" + n1 + ") = " + resultLoop);
        System.out.println("Loop time: " + (endLoop - startLoop) + " ns");

        // Timing using loop and 25!        
        long startLoop2 = System.nanoTime();
        long resultLoop2 = factorial_loop(n2);
        long endLoop2 = System.nanoTime();
        System.out.println("Loop factorial(" + n2 + ") = " + resultLoop2);
        System.out.println("Loop time: " + (endLoop2 - startLoop2) + " ns");

        // Timing using loop and 50!, shows error
        long startLoop5 = System.nanoTime();
        long resultLoop5 = factorial_loop(n3);
        long endLoop5 = System.nanoTime();
        System.out.println("Loop factorial(" + n3 + ") = " + resultLoop5);
        System.out.println("Loop time: " + (endLoop5 - startLoop5) + " ns");

        // Timing using recursion and 15!
        long startRec = System.nanoTime();
        long resultRec = factorial_recurse(n1);
        long endRec = System.nanoTime();
        System.out.println("Recursive factorial(" + n1 + ") = " + resultRec);
        System.out.println("Recursive time: " + (endRec - startRec) + " ns");

        // Timing using recursion and 25!
        long startRec2 = System.nanoTime();
        long resultRec2 = factorial_recurse(n2);
        long endRec2 = System.nanoTime();
        System.out.println("Recursive factorial(" + n2 + ") = " + resultRec2);
        System.out.println("Recursive time: " + (endRec2 - startRec2) + " ns");

        // Timing using recursion and 50!, shows error
         long startRec6 = System.nanoTime();
        long resultRec6 = factorial_recurse(n3);
        long endRec6 = System.nanoTime();
        System.out.println("Recursive factorial(" + n3 + ") = " + resultRec6);
        System.out.println("Recursive time: " + (endRec6 - startRec6) + " ns");


        // Timing using loop and 100! with BigInt
     long startLoop3 = System.nanoTime();
        BigInteger resultLoop3 = BigInt_loop(n4);
        long endLoop3 = System.nanoTime();
        System.out.println("Loop factorial(" + n4 + ") is " + resultLoop3);
        System.out.println("Loop time: " + (endLoop3 - startLoop3) + " ns");

        // Timing using recursion and 100! with BigInt
        long startRec4 = System.nanoTime();
        BigInteger resultRec4 = BigInt_recurse(n4);
        long endRec4 = System.nanoTime();
        System.out.println("Recursive factorial(" + n4 + ") = " + resultRec4);
        System.out.println("Recursive time: " + (endRec4 - startRec4) + " ns");

    }
}
