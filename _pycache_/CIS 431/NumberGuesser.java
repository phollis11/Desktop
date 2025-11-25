import java.util.Random;
import java.util.Scanner;

public class NumberGuesser {
    public static void main(String[] args) {
        game();
    }

    public static void game() {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();

        System.out.println("Welcome to the game");
        System.out.println("I am thinking of a number 1-100");

        int randomNum = random.nextInt(100) + 1; // 1–100
        int attempts = 0;
        int guess = -1;

        while (guess != randomNum) {
            System.out.print("Guess a number 1-100: ");
            try {
                guess = Integer.parseInt(scanner.nextLine());
                attempts++;

                if (guess < randomNum) {
                    System.out.println("Too small, try again");
                } else if (guess > randomNum) {
                    System.out.println("Too large, try again");
                } else {
                    System.out.println("Congrats, it took " + attempts + " attempts!");
                }
            } catch (NumberFormatException e) {
                System.out.println("Please enter a valid number");
            }
        }

        scanner.close();
    }
}
