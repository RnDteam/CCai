package Server;

import java.io.*;
import java.net.*;

public class HebMorphClient 
{
	public static void main(String[] args) throws IOException 
	{
		int port = 4444;

		Socket echoSocket = null;
		PrintWriter out = null;
		BufferedReader in = null;
		String hostName = "127.0.0.1";

		try 
		{
			echoSocket = new Socket(hostName, port);
			out = new PrintWriter(echoSocket.getOutputStream(), true);
			in = new BufferedReader(new InputStreamReader(echoSocket.getInputStream()));
		} 
		catch (UnknownHostException e) 
		{
			System.err.println("Don't know about host: " + hostName);
			System.exit(1);
		} 
		catch (IOException e) 
		{
			System.err.println("Couldn't get I/O for the connection to: " + hostName);
			System.exit(1);
		}

		BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in));
		String userInput;

		userInput = "אני רוצה לאפס את הסיסמה.";
		while ((userInput = stdIn.readLine()) != null) 
		{
			out.println(userInput);
			System.out.println("echo: " + in.readLine());
		}

		out.close();
		in.close();
		stdIn.close();
		echoSocket.close();
	}
}

