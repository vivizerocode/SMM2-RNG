
import java.util.Scanner;


public class Main {
  public static void main(String[] args) {
    RNG.Init();
    System.out.println("Hex X value");
    Scanner input = new Scanner(System.in);
    String hex = input.nextLine();
    Long target = Long.parseLong(hex,16);
    System.out.println("Integer Value = " + target);  
    RNG.RunUntilMatch(target);
   
    };
  }


