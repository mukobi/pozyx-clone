package psupozyx;

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
import java.util.ResourceBundle;

public class ConsoleWindow implements Initializable {
    @FXML
    private Label console;

    private Process pr;
    
    private static final int CHARACTERDISPLAYBUFFER = 30000;

    void launchPyScript(String py_script_name) {
        new Thread(() -> {
            try {
                console.setText("");
                ProcessBuilder ps=new ProcessBuilder("python", "-u", py_script_name);

                ps.redirectErrorStream(true);

                pr = ps.start();
                InputStream inputStream = pr.getInputStream();

                BufferedReader in = new BufferedReader(new InputStreamReader(inputStream), 2048);
                String line;
                String pooledOutput;


                int timePos;
                float pyElapsedTime;

                double delayTime = 3.0;

                long newTime;
                long nanodifference;
                long oldTime = System.nanoTime();
                float secondDif;


                // read python script output
                while ((line = in.readLine()) != null) {

                    /*
                    // if the line has time information
                    if (line.contains(" Time: ")) {
                        // is a data line
                        timePos = line.indexOf("Time:");
                        pyElapsedTime = 1 * Float.parseFloat((line.substring(timePos + 6, timePos + 16)));


                        newTime = System.nanoTime();
                        nanodifference = newTime - oldTime;
                        secondDif = (float) (nanodifference / 1000000000.0);
                        // Thread.sleep(5);
                        while (secondDif < (pyElapsedTime + delayTime)) {
                            newTime = System.nanoTime();
                            nanodifference = newTime - oldTime;
                            secondDif = (float) (nanodifference / 1000000000.0);
                            Thread.sleep(5);
                        }

                    } else {
                        Thread.sleep(30);
                    }
                    */

                    //Thread.sleep(10);
                    // add input line to the top of the console Label

                    pooledOutput = line + '\n' + console.getText();
                    if(pooledOutput.length() >= CHARACTERDISPLAYBUFFER) {
                        pooledOutput = pooledOutput.substring(0, CHARACTERDISPLAYBUFFER);
                    }
                    final String finalOutput = pooledOutput;
                    javafx.application.Platform.runLater( () -> console.setText(finalOutput));



                    // for debugging
                    System.out.println(String.valueOf(line));
                }
                pr.waitFor();

                in.close();

            } catch (IOException | InterruptedException e) {
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
