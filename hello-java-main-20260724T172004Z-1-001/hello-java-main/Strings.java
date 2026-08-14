import java.util.Locale;

public class Strings {

    public static void main(String[] args){

        // Cadenas de texto

        String name = "hola";
        var surname = new String("hela");

        // operaciones basicas
        System.out.println(name);
        System.out.println(name+surname);
        //Concatenacion
        System.out.println(name+" "+surname);

        //logitud

        System.out.println(name.length());

        //obtener caracter

        System.out.println(name.charAt(0));
        //obtener sin necesidad del indice.
        System.out.println(name.charAt(name.length()-1));


        //obtener una subcadena

        System.out.println(name.substring(2));
        System.out.println(name.substring(1,3));

        //MAYUSCULAS y minusculas

        System.out.println(name.toUpperCase());
        System.out.println(name.toLowerCase());

        System.out.println(name);

        //contenerdores, si contiene algo.

        System.out.println("hola, java".contains("jaja"));
        System.out.println("hola, java".contains("ava"));
        System.out.println("hola, java".toUpperCase().contains("AVA"));


        //Comparaciones

        System.out.println(name.equals("hola"));
        System.out.println(name.equals("HOLA"));
        System.out.println(name.equalsIgnoreCase("HOLA"));

        // == vs SQUALS

        var a = "Brais";
        var b = "Brais";

        var c = new String("Brais");

        System.out.println(a==b);
        System.out.println(a==c);
        System.out.println(a.equals(c));

        //Trim operacion para modificar o eliminar caracteres

        System.out.println("Hola me llamo Brais".trim());
        System.out.println(" Hola me llamo Brais ");

        // replace

        System.out.println("Hola me llamo Brais".replace("Brais", "Mundo"));

        //format
        //%s para formatear cadenas de texto
        //%d para formatear numeros enteros
        //%f para formatear  numeros decimale
        var age = 1000;
        System.out.println(String.format("Hola me llamo mundo con 1000 años", name, age));
        System.out.println(String.format("Hola me llamo %s con %d", name, age));




    }
}
