# Instruction to download ISMP6 data
<div style="background-color:rgb(251, 251, 251); color: #721c24; border: 1px solid #f5c6cb; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
</div>
<br>

The purpose of this file is to help you download all ISMP6 simulation to replicate the work done in the following steps. 
The instruction provided are for Unix.

## Obtaining ISMP6 datasets
Download the data using Globus Connect Personnal
Install the appropriete version of the app for your computer then do the following steps:

- Create an account
- Create your own server with the path you want to save your data into
- Connect to ther server `GHub-ISMIP6-Projections-2300`
- Start a download requests

>[!NOTE]
>You can also use you terminal to download the data.
>But it can rise error if you do not have the capacity to open a navigator window inside it.
>In addition is you are on the UGA campus the connection to Globus will be bloced.

If you want to use you terminal, follow those step:

1. Install `globus`
In you local terminal or a Jupyterhub terminal, follow these steps:

- Install `pipx`
```
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```
_Note: depending on your python and pip version the command might be_ `python3 -m pip3 install --user pipx`

Close and re-open your current shell or open a new one, then do:
```
pipx install globus-cli
```
- Log in to Globus
Use the following command:
```
globus login --no-local-server
```
Copy the provided link and log in to globus using the same plateform as you Ghub account.
You will than recieve a authentification code, copy-paste it into the terminal.
_You can find more infomation to login on:_ https://docs.globus.org/cli/quickstart/

2. Install Globus Personal Connect
Run the following commands:
```
 wget https://downloads.globus.org/globus-connect-personal/linux/stable/globusconnectpersonal-latest.tgz
 tar xzf globusconnectpersonal-latest.tgz
```
_If the command doesn't work, install_`wget` _using_ `brew install wget`

Then go to the newly created directory:
```
cd globusconnectpersonal-3.2.6
```
_Note: your directory name can be different._

Run globusconnectpersonal:

```
./globusconnectpersonal
```
_if this command doesn't work than do_

Then do
```
export PATH=/home/user/globusconnectpersonal-3.2.6:$PATH
```

Start the Globus Personal Connect client:
```
globusconnectpersonal -start &
```

Test a transfer of one of the ISMIP6 README files to the current directory:
```
globus transfer 'ad1a6ed8-4de0-4490-93a9-8258931766c7:/GrIS/Ocean_Forcing/README_GrIS_Ocean_Forcing.txt' `globus endpoint local-id`:./README_GrIS_Ocean_Forcing.txt
```

If everything works correctly—congrats! Now it's time to download the ISMP6 datasets.

3. Downloading the ISMP6 datasets
We'll use the `GHub-ISMIP6-Projections-2300` dataset that have `3881e705-3290-4e81-8990-0ef8cfb54d74`as ID

-   Save the simulations name
We'll download all the simulations of the `GHub-ISMIP6-Projections-2300`, therefore we'll use the following command:
```
globus ls '3881e705-3290-4e81-8990-0ef8cfb54d74:/' > name.txt
```

- Downloading datasets
Using python file `ISMP6_download.py` and entering the path of the directory where `name.txt` was created it will download all the datasets used in the project.
```
python ./ISMP6_download.py
```
_please make sure you have numpy installed_

Now that you have download datasets, you'll need to creat a specific conda environment in order to reproduce the work.


## Creat a Conda environment
If you already have `conda` skip part 1
Assuming you already have `brew` installed on you computer, 
1. Start the by downloading conda via Microconda:
```
brew install --cask miniconda
```

Verify that 'anaconda' was installed correctly do:
```
conda --version
```

In order to activate conda, you'll need to close and re-open your current shell or open another one, than do:
```
conda init
conda activate
```

Great you succesfully installed conda and entered the conda environent!

2. Create the ISMP6 environment
Let's now creat a `conda` environment to be able to redo the analysis, this environment will be named `ISMP6`. 
In you terminal after activating conda and downloading the `env.yml` (in the repertory) do the following steps:

```
conda env create -f env.yml
conda activate ISMP6
conda env list
```