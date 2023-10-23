# JupyterOcean Extension

The JupyterOcean Library currently comprises of a Jupyter Lab extension for using MetaMask within Jupyter Lab to interact with the [Ocean market](https://market.oceanprotocol.com/), and use the decentralized storage to store data scientist raw asset files (Infura IPFS for decentralized storage).

## 🏗 Setup

To start using the extension, simply run these commands in your terminal::
( Note: if the `jupyter labextension` failed with the extension not found error, try to reload the IDE and run again. )

```
git clone https://github.com/Han-Linnn/JupyterOcean.git

cd JupyterOcean/

conda create -n jupyterocean -c conda-forge jupyterlab ipylab jupyter-packaging nodejs ipytree bqplot ipywidgets numpy

conda activate jupyterocean

python -m pip install -e ".[dev]"

jupyter labextension develop . --overwrite

jlpm

jlpm run build

jupyter lab

```

After any changes, run `jlpm run build` to see them in Jupyter Lab. Note that you might need to run `jlpm` or `python -m pip install -e ".[dev]"` depending on whether you add new dependencies to the project.

## 📚 Usage

### Init:

```
from jupyterOcean import JupyterFrontEnd
app = JupyterFrontEnd()
```

### Connect to Metamask:

You can either click the `JupyterOcean` pannel on the menu and execute the `connect wallet` option to connect Metamask wallet or run the following command:

```
app.commands.execute('connect_wallet')
```

### Send OCEAN and tokens to virtual wallet:

You can either click the `JupyterOcean` pannel on the menu and execute the `send ocean` option to send OCEAN and tokens to virtual wallet or run the following command:

```
app.commands.execute('send_ocean')
```

### Convert notebook to Compute-to-data(C2D) format Python script:

```
app.ocean.convert(<notebook_path>)
```

### Store asset on IPFS:

Click the `JupyterOcean` pannel on the menu and execute the `IPFS Storage` option to save file on IPFS and get CID hash.

### Publish asset to Ocean Market:

Run the following command and input the IPFS CID `cid` and the asset name `name` you want to use on Ocean Market.
If you want to publish the dataset to run the C2D on Ocean Market, you can authorize the target algorithm for the dataset you publish by adding extra param `algo_did`.

```
// For dataset
app.ocean.dt_publish(<cid>, <asset name>, <OPTION: algo_did>)

// For algorithm
app.ocean.at_publish(<cid>, <asset name>)
```

### Download asset from Ocean Market:

Run the following command and input the DID of target asset to download the asset.

```
// For dataset
app.ocean.buy_dt_download(<did>)

// For algorithm
app.ocean.buy_at_download(<did>)
```

### Run Compute-to-data on Ocean Market:

Run the following command and input the DIDs of target dataset and algorithm to run the compute job online and get the result model.

```
\\ For running assets published through JupyterOcean
app.ocean.temp_c2d(<dataset_did>, <algorithm_did>)

\\ For running assets published through UI
app.ocean.c2d(<dataset_did>, <algorithm_did>)
```
