# Mive AT-M130 Research (Cinnamoroll Kids Phone)

![Mive AT-M130](https://www.altech.kr/data/goodsImages/GOODS1_1704358156.png)

This project aims to analyze the Mive Cinnamoroll Kids Phone and ZEM Pokemon edition 2 Kids Phone (Model: AT-M130).
This device is branded by Mive (ALT) and manufactured by the Chinese ODM company Chinoe.

## Device Specifications

| Category | Details |
| :--- | :--- |
| **Processor** | Qualcomm Snapdragon 685 SoC (Octa-core 2.8GHz CPU, Adreno GPU) |
| **Display** | 5.8-inch HD+ (1560×720) IPS LCD (268 ppi) |
| **Camera** | Front: 13MP / Rear: 50MP + 5MP (Dual LED Flash) |
| **Memory** | 6GB RAM, 128GB ROM |
| **Network** | LTE, WCDMA |
| **Connectivity** | Wi-Fi 802.11 a/b/g/n/ac, Bluetooth 5.1 |
| **Ports** | USB Type-C, 3.5mm Headphone Jack |
| **Body** | 69.5 x 146.8 x 8.5 mm, 162g (Metal frame) |
| **Colors** | Pokémon Edition / Cinnamoroll Edition |
| **Battery** | Li-Ion 3350 mAh (Non-removable) |
| **OS** | Android 13 |
| **Biometrics** | Face Recognition |
| **Others** | IP68 Water/Dust Resistance, SAR Head 0.785 W/kg |

## Firmware Acquisition & EDL Dump

Since the manufacturer does not officially provide stock firmware, the initial goal of this project was to acquire the firmware image.
I successfully obtained a full firmware dump using a modified Qualcomm EDL Firehose loader.

- **Partition Table**: See [GPT.md](GPT.md) for the partition layout retrieved via the loader.
- **Secure Boot Status**: The device ships with Secure Boot disabled by default.
  - This critical configuration allowed us to bypass authentication requirements (VIP EDL programming was not implemented), enabling the use of a modified/unsigned Firehose loader to dump the storage.

## FOTA & OTA Analysis

The device utilizes the **Adups FOTA solution** for software updates.

- **OTA Limitation**: The manufacturer only pushes incremental updates, meaning there is no direct way to obtain a full OTA package through standard channels.
- **Protocol Analysis**:
  - The protocol analysis and the Python script (`adups_key hasher.py`) are adapted from [TBT8A10/adups-fota](https://github.com/TBT8A10/adups-fota). Relevant parts were extracted and modified to work with this device.
  - The script generates the specific encrypted `key` required by the server.
  - By sending a POST request with this generated key to the URL mentioned in the script, I can retrieve OTA download links and additional metadata.
  - **Note**: It was observed that if the `appCode` parameter is set to **315** or higher, the OTA download URL changes from `hwfotadown.mayitek.com` to `lensdown.mayitek.com`.

## File Description

### `adups_key hasher.py`

A Python script to generate and decrypt the payload for the Adups FOTA server (`fota5p.adups.com`).

**Features:**

- `encode_data(s)`: Encrypts the string according to the Adups protocol (XOR, bit shifting, random byte padding).
- `decode_data(key)`: Decrypts the hex string back to plaintext.
- `generate_post_data(config)`: Constructs the body data for the POST request.

## Usage

Requires Python 3.

```bash
python "adups_key hasher.py"
```

Running the script outputs the encoded data based on the parameters (e.g., `&appCode=0&project=...`) defined in `main()`.

## Disclaimer

This project is for research and educational purposes only. I am not responsible for any issues arising from the unauthorized use of this code or information.
