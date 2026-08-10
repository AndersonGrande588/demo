public class Operadores {

    public static void main(String[] args){

        //operadores

        //Aritméticos
         var a = 5;
         var b = 3;
         System.out.println(a + b);
         System.out.println(a - b);
         System.out.println(a * b);
         System.out.println(a / b);
         System.out.println(a % b);

         // Asignación
        a = b ;
        System.out.println(a);

        a = b * 2;
        System.out.println(a);

        a += 1;  // a = a + 1
        System.out.println(a);
        a -= 1;
        System.out.println(a);
        a *= 1;
        System.out.println(a);
        a /= 1;
        System.out.println(a);
        a %= 1;
        System.out.println(a);

        //comparacion(relacionales)

        System.out.println(a == b);
        System.out.println(a == 6);
        System.out.println(a == 0);
        System.out.println(a != b);
        System.out.println(a > b);
        System.out.println(a >= b);
        System.out.println(a < b);
        System.out.println(a <= b);

        //LOGICOS
       // Y(&&) = (AND)
        System.out.println(true && true);
        System.out.println(true && false);
        System.out.println(false && true);
        System.out.println(false && false);

        System.out.println(3 > 2 && 5 == 2);

        // O(||) = (OR)
        System.out.println(true || true);
        System.out.println(true || false);
        System.out.println(false || true);
        System.out.println(false || false);

        System.out.println(3 > 2 || 5 == 2);

        // NO(!) = (NOT)
        System.out.println(!true);
        System.out.println(!false);
        System.out.println(!(3 > 2) || 5 == 2);

        //Unarios
        System.out.println(+b);
        System.out.println(-b);
        System.out.println(b++);
        System.out.println(++b);
        System.out.println(b--);
        System.out.println(--b);
        System.out.println("-------------------");

        int c = 1;

        System.out.println(+c);
        System.out.println("-------------------");
        System.out.println(-c);
        System.out.println("-------------------");
        System.out.println(c++);
        System.out.println("-------------------");
        System.out.println(++c);
        System.out.println("-------------------");
        System.out.println(c--);
        System.out.println("-------------------");
        System.out.println(--c);
        System.out.println("-------------------");

    }
}
