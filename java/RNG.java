import java.util.ArrayList;
import java.util.List;

public class RNG {
    static long x, y, z, w;
    static long c;

    public static List<Long> RNGStates = new ArrayList<>();

    public static void Init() {
        c = 0;
        x = ARNGPlus(0);
        y = ARNGPlus(x);
        z = ARNGPlus(y);
        w = ARNGPlus(z);
        RNGStates.add(w);
    }

    public static long ARNGPlus(long input) {
        long m = input ^ (input >> 30);
        c++;
        long output = ((m * 0x6C078965L) + c) & 0xFFFFFFFFL;
        return output;
    }

    public static long Xorshift() {
        long t = x ^ ((x << 11) & 0xFFFFFFFFL);
        long newW = w ^ (w >> 19) ^ (t ^ (t >> 8));


        x = y;
        y = z;
        z = w;
        w = newW;

        RNGStates.add(w);

        return w;
    }

    public static long GetRandomNumber(int X) {
        long w;
        if (X < RNGStates.size()) {
            w = RNGStates.get(X);
        } else {
            w = Xorshift();
        }
        return w;
    }
    public static void RunUntilMatch(long target) {
        long randomNumber;
        int attempts = 0;
        do {
            randomNumber = Xorshift();
            attempts++;
           
        } while (randomNumber != target);
        System.out.println("X = " + (attempts + 1));
    }

}
