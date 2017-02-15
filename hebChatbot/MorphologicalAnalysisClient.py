import requests
import socket

# ENCODING_TYPE = "UTF-8"
ENCODING_TYPE = "ISO-8859-8"


class MorphologicalAnalysisClient:
    HOST = "localhost"
    PORT = 4444
    CHATBOT_URL = 'http://' + HOST + ":" + str(PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    @staticmethod
    def connect_morphological_analysis():
        MorphologicalAnalysisClient.sock.connect((MorphologicalAnalysisClient.HOST, MorphologicalAnalysisClient.PORT))

    @staticmethod
    def get_morphological_analysis_message(message):
        MorphologicalAnalysisClient.sock.sendall(bytes(message + '\n', ENCODING_TYPE))
        data = MorphologicalAnalysisClient.sock.recv(1024)
        text = (data.decode(ENCODING_TYPE))
        words = text.replace("^"," ")
        print(words)
        return words
    """
        	String answerToClient = "";
        	Charset UTF8_CHARSET = Charset.forName("UTF-8");
        	byte [] bt = inputLine.getBytes();
        	inputLine = new String(bt, UTF8_CHARSET);
        	System.out.println("received input line: " + inputLine);
        	System.out.println(inputLine.length());
        	"""