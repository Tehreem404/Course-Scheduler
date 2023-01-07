### CIS-3760

# Navigating our Website

* the link to our website is: https://3.141.107.243/
* to switch between semesters select either the F22 or W23 buttons at the top of the page
* The table will have all the courses in the semester loaded into it
* To search courses it needs to be in the form of: `CIS` or `CIS*3760` or `CIS*0103`
    * Note - doesn't have to be CIS courses this was just an example of the format
* to get reccomended courses it works best on an already searched result
* To Add a course click the add button beside the course in the course table
* All your selected courses will show up in a list of cards below the table. There is a remove button on each card if you would like to remove the course.
* To view your course schedule on the selected courses click the 'create schedule' button below your selected courses

# Instructions - How to Configure and Run Server
1. From your local command prompt, run `git clone https://gitlab.socs.uoguelph.ca/rmohl/cis-3760.git` to download the SSH key needed.
>If you are on MAC OS Run following command before running step 2
>> `chmod 400 "cis-3760/configuration/cis-3760-key-pair.pem` 
>
>If you are on windows or a Linux WSL for windows you will need to manually change file properties
>>Navigate to the folder you just cloned into via the file explorer <br>
>>In the configuration folder right click on the .pem file <br>
>>Choose properties <br>
>>Navigate to the security tab <br>
>>Choose Advanced <br>
>>Disable inheritance <br>
>>Click on Users (it should be now highlighted in blue) <br>
>>Choose the remove option and click apply. <br>
>>You should now be able to proceed to step 2 <br>
2. SSH to your EC2 instance. From your local command prompt, run `ssh -i "cis-3760/configuration/cis-3760-key-pair.pem" ubuntu@dns-address`
> Demo DNS Address: ec2-18-191-15-176.us-east-2.compute.amazonaws.com <br>
> Test DNS Address: ec2-3-142-153-165.us-east-2.compute.amazonaws.com
3. You should now be sshed into your EC2 instance. Now, to clone the git repository to your EC2 instance, run `git clone https://gitlab.socs.uoguelph.ca/rmohl/cis-3760.git`.
4. Run `cd cis-3760 `to enter the project and `git checkout sprint-5` to checkout this week's work.
5. Run `bash ./installScriptUbuntu.sh `to install dependancies and configure the web server. You can continue the script by entering "y" when prompted by text, or by selecting "Ok" when prompted with a menu.
6. Run `bash ./installScriptFlask.sh` to install dependancies for back end of web server (flask/gunicorn).
7. After the installation scripts end, navigate to the URL where your instance is running
> Demo DNS URL: ec2-18-191-15-176.us-east-2.compute.amazonaws.com <br>
> Test URL: 3.142.153.165

8. Select the EC2 instance you ssh'd into, and copy and paste the Public IPv4 address, or the public IPv4 DNS to the search bar.
9. You should see the react application.

# Instructions - How to Stop & Restart Server
1. SSH to your EC2 instance. From your local command prompt, navigate to your project folder and run `ssh -i "/cis-3760/configuration/cis-3760-key-pair.pem" ubuntu@dns-address`.
> Demo DNS Address: ec2-18-191-15-176.us-east-2.compute.amazonaws.com <br>
> Test DNS Address: ec2-3-142-153-165.us-east-2.compute.amazonaws.com
2. Run `sudo systemctl stop nginx` to stop the nginx server.
3. Run `sudo systemctl start nginx` to start the nginx server. 
