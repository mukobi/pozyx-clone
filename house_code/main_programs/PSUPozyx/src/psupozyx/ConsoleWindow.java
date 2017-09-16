package psupozyx;

import javafx.application.Platform;
import javafx.concurrent.Task;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.stage.Stage;
import sun.rmi.log.LogOutputStream;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.Arrays;
import java.util.Objects;
import java.util.ResourceBundle;

public class ConsoleWindow implements Initializable {
    @FXML
    private Label console;

    private Process     pr;
    
    private static final int CHARACTERDISPLAYBUFFER = 30000;

    void launchPyScript(String startMessage, String executable, String prependPathType) {
        if (startMessage != null) {
            console.setText(startMessage);
        }
        String osName = System.getProperty("os.name");
        console.setText("Running " + executable + " on " + osName + '\n');
        new Thread(() -> {
            try {
                String executableWithDirectory = executable;
                if (osName.startsWith("Windows")) {
                    if(Objects.equals(prependPathType, "COMPILEDPATH")) {
                        executableWithDirectory = "build/exe.win32-3.6/" + executableWithDirectory;
                    }
                }


                ProcessBuilder ps=new ProcessBuilder(executableWithDirectory);

                ps.redirectErrorStream(true);

                pr = ps.start();
                InputStream inputStream = pr.getInputStream();

                BufferedReader in = new BufferedReader(new InputStreamReader(inputStream), 2048);
                String line;
                String pooledOutput;

                // read python script output
                while ((line = in.readLine()) != null) {

                    pooledOutput = line + '\n' + console.getText();
                    if(pooledOutput.length() >= CHARACTERDISPLAYBUFFER) {
                        pooledOutput = pooledOutput.substring(0, CHARACTERDISPLAYBUFFER);
                    }
                    final String finalOutput = pooledOutput;
                    Platform.runLater( () -> console.setText(finalOutput));
                }
                pr.waitFor();

                in.close();

            } catch (IOException | InterruptedException e) {
                console.setText(e.toString() + console.getText());
                e.printStackTrace();
            }
        }).start();
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
    }

    void terminateProcess() {
        if (pr != null) {
            pr.destroy();
        }
    }
}
