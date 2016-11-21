package customcontrolexample;


import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

/**
 * Created by meltzer on 21/11/2016.
 */
public class Utils {
    public static BufferedImage refreshCAPTCHA(){
        return null;
    }
    public static boolean sendCAPTCHA(String userInput){
        return true;
    }
    public static BufferedImage browseImage(String path)
    {
        BufferedImage img = null;

        try
        {
            img = ImageIO.read(new File("C:/ImageTest/pic2.jpg")); // eventually C:\\ImageTest\\pic2.jpg
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
        return img;

    }
    public static boolean sendImage(BufferedImage BufferedImageImage)
    {
        return true;
    }
    public static boolean sendCredentials(String username, String password)
    {
        return true;
    }
    public static boolean changePassword(String password , String newPassword)
    {
    return true;
    }
    public static boolean updateImage(BufferedImage newImage)
    {
        return true;
    }
    public static int[] downloadStats()
    {
        return null;
    }
}
