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

        System.out.println();
    }
}
