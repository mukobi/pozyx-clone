package psupozyx;

import javafx.application.Platform;
import javafx.concurrent.Task;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.stage.Stage;
import sun.reflect.generics.reflectiveObjects.NotImplementedException;
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

    private String osName = System.getProperty("os.name");
    private String OS = osName.toLowerCase();

    void launchPyScript(String startMessage, String executable, String prependPathType) {
        if (startMessage != null) {
            console.setText(startMessage);
        }

        console.setText("Running " + executable + " on " + osName + '\n');
        new Thread(() -> {
            try {
                String executableWithDirectory = executable;
                if (isWindows()) {
                    if(Objects.equals(prependPathType, "COMPILEDPATH")) {
                        executableWithDirectory = "build/exe.win32-3.6/" + executableWithDirectory + ".exe";
                    }
                    else if(Objects.equals(prependPathType, "PYINSTALLERPATH")) {
                        executableWithDirectory = "dist/" + executableWithDirectory + "/" + executableWithDirectory + ".exe";
                    }
                }
                else if (isMac()) {
                    if(Objects.equals(prependPathType, "COMPILEDPATH")) {
                        executableWithDirectory = "build/exe.macosx-10.6-intel-3.6/" + executableWithDirectory;
                    }
                    else if(Objects.equals(prependPathType, "PYINSTALLERPATH")) {
                        executableWithDirectory = "dist/" + executableWithDirectory + "/" + executableWithDirectory + ".app";
                    }
                }
                else if (isUnix()) {
                    if(Objects.equals(prependPathType, "COMPILEDPATH")) {
                        executableWithDirectory = "build/exe.linux-i686-3.5/" + executableWithDirectory;
                    }
                }
                else {
                    console.setText("Unfortunately your operating system is not yet supported.\n" +
                            "Please try again on a Windows, Mac, or Linux device.");
                    throw new NotImplementedException();
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


    private boolean isWindows() {
        return (OS.contains("win"));
    }

    private boolean isMac() {
        return (OS.contains("mac"));
    }

    private boolean isUnix() {
        return (OS.contains("nix") || OS.contains("nux") || OS.indexOf("aix") > 0 );
    }

    private boolean isSolaris() {
        return (OS.contains("sunos"));
    }
}
