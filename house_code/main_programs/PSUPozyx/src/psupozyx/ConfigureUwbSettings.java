package psupozyx;

import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.CheckBox;
import javafx.scene.control.ChoiceBox;
import javafx.stage.Stage;
import javafx.stage.StageStyle;

import java.io.IOException;

public class ConfigureUwbSettings {

    @FXML
    private ChoiceBox<String> m_channel;
    @FXML
    private ChoiceBox<String> m_bitrate;
    @FXML
    private ChoiceBox<String> m_prf;
    @FXML
    private ChoiceBox<String> m_plen;
    @FXML
    private ChoiceBox<String> m_gain;

    @FXML
    private CheckBox m_show_console_output;


    public void handleLaunchConfigureUwb(ActionEvent actionEvent) {
        String channel = m_channel.getValue().toString();

        String unparsedBitrate = m_bitrate.getValue();
        String bitrate = "0";
        switch (unparsedBitrate) {
            case "110 Mbps":
                bitrate = "0";
                break;
            case "850 Mbps":
                bitrate = "1";
                break;
            case "6810 Mbps":
                bitrate = "2";
                break;
            default:
                bitrate = "1";
                break;
        }

        String unparsedPrf = m_prf.getValue().toString();
        String prf = "0";
        switch (unparsedPrf) {
            case "16 MHz":
                prf = "1";
                break;
            case "64 MHz":
                prf = "2";
                break;
            default:
                prf = "2";
                break;
        }

        String unparsedPlen = m_plen.getValue().toString();
        String plen = "0";
        switch (unparsedPlen) {
            case "64":
                plen = "0x04";
                break;
            case "128":
                plen = "0x14";
                break;
            case "256":
                plen = "0x24";
                break;
            case "512":
                plen = "0x34";
                break;
            case "1024":
                plen = "0x08";
                break;
            case "1536":
                plen = "0x18";
                break;
            case "2048":
                plen = "0x28";
                break;
            case "4096":
                plen = "0x0C";
                break;
            default:
                plen = "0x08";
                break;
        }

        String gain = m_gain.getValue();

        boolean showConsole = m_show_console_output.isSelected();

        launchConsoleLogging(new String[]{"python", "-u", "configure_uwb_settings.py", channel, bitrate, prf, plen, gain}, showConsole);
    }

    public void handleMaximumRange(ActionEvent actionEvent) {
        m_bitrate.setValue("110 Mbps");
        m_plen.setValue("4096");
        m_gain.setValue("33.5");
    }

    public void handleFavorRange(ActionEvent actionEvent) {
        m_bitrate.setValue("110 Mbps");
        m_plen.setValue("2048");
        m_gain.setValue("25.0");
    }

    public void handleBalanced(ActionEvent actionEvent) {
        m_bitrate.setValue("850 Mbps");
        m_plen.setValue("1024");
        m_gain.setValue("15.0");
    }

    public void handleFavorDataRate(ActionEvent actionEvent) {
        m_bitrate.setValue("6810 Mbps");
        m_plen.setValue("256");
        m_gain.setValue("5.0");
    }

    public void handleMaximumDataRate(ActionEvent actionEvent) {
        m_bitrate.setValue("6810 Mbps");
        m_plen.setValue("64");
        m_gain.setValue("0.0");
    }

    public void handleQuit(ActionEvent actionEvent) {
        Platform.exit();
    }

    private void launchConsoleLogging(String[] pythonCommands, boolean showConsole) {
        try {
            Stage stage = new Stage();
            FXMLLoader loader = new FXMLLoader(getClass().getResource("fxml/console_window.fxml"));
            Parent root1 = loader.load();
            stage.setTitle("UWB Configuration Output");
            stage.setScene(new Scene(root1));
            stage.setMaximized(false);
            stage.initOwner(m_channel.getScene().getWindow());
            stage.initStyle(StageStyle.DECORATED);
            ConsoleWindow console_controller = loader.getController();
            stage.setOnCloseRequest(we -> {
                console_controller.terminateProcess();
            });
            if (showConsole) {
                stage.show();
            }

            console_controller.launchPyScript("Setting UWB settings. Feel free to close when done.", pythonCommands);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
