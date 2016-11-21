package customcontrolexample;

/**
 * Created by meltzer on 21/11/2016.
 */
import java.io.IOException;

import javafx.beans.property.StringProperty;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
public class MainVC extends VBox{
public MainVC()
{
    FXMLLoader fxmlLoader = new FXMLLoader(getClass().getResource("main_screen.fxml"));
    fxmlLoader.setRoot(this);
    fxmlLoader.setController(this);

    try {
        fxmlLoader.load();
    } catch (IOException exception) {
        throw new RuntimeException(exception);
    }
}
    @FXML
    protected void changePass() {
        System.out.println("The button was clicked!");
    }
}
