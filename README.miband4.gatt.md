# miband4 BLE protocol

## Get different UUIDs

1. it is best to stop miband-api service
2. on host machine start `sudo bluetoothctl`
3. connect to the miband device using its mac address (e.g. `connect D1:C5:15:51:03:89`)
4. enter command `info`

```sh
[Mi Smart Band 4]# info
Device D1:C5:15:51:03:89 (public)
        Name: Mi Smart Band 4
        Alias: Mi Smart Band 4
        Paired: no
        Trusted: no
        Blocked: no
        Connected: yes
        LegacyPairing: no
        UUID: Vendor specific           (00001530-0000-3512-2118-0009af100700)
        UUID: Generic Access Profile    (00001800-0000-1000-8000-00805f9b34fb)
        UUID: Generic Attribute Profile (00001801-0000-1000-8000-00805f9b34fb)
        UUID: Immediate Alert           (00001802-0000-1000-8000-00805f9b34fb)
        UUID: Device Information        (0000180a-0000-1000-8000-00805f9b34fb)
        UUID: Heart Rate                (0000180d-0000-1000-8000-00805f9b34fb)
        UUID: Alert Notification Serv.. (00001811-0000-1000-8000-00805f9b34fb)
        UUID: Unknown                   (00003802-0000-1000-8000-00805f9b34fb)
        UUID: Anhui Huami Information.. (0000fee0-0000-1000-8000-00805f9b34fb)
        UUID: Anhui Huami Information.. (0000fee1-0000-1000-8000-00805f9b34fb)
        Modalias: bluetooth:v0157p0024d0101
        ManufacturerData Key: 0x0157
        ManufacturerData Value:
  02 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff  ................
  ff 02 d1 c5 15 51 03 89                          .....Q..        
        RSSI: -68
```

## info about characteristics fetch and activity data

Use bluetoothctl to connect to miband, enter `menu gatt` and then enter below command in bluetootctl:

**CHARACTERISTIC_FETCH**  = `00000004-0000-3512-2118-0009af100700`

```sh
[bluetooth]# attribute-info 00000004-0000-3512-2118-0009af100700
Characteristic - Vendor specific
        UUID: 00000004-0000-3512-2118-0009af100700
        Service: /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a
        Notifying: no
        Flags: write-without-response
        Flags: notify
```

**CHARACTERISTIC_ACTIVITY_DATA** = `00000005-0000-3512-2118-0009af100700`

```sh
[bluetooth]# attribute-info 00000005-0000-3512-2118-0009af100700
Characteristic - Vendor specific
        UUID: 00000005-0000-3512-2118-0009af100700
        Service: /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a
        Notifying: no
        Flags: notify
```

## list all attributes

Once connected to miband device using `bluetoothctl` enter following commands:

```sh
menu gatt
list-attributes
```

```sh
[Mi Smart Band 4]# list-attributes
Primary Service (Handle 0x0009)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0008
        00001801-0000-1000-8000-00805f9b34fb
        Generic Attribute Profile
Primary Service (Handle 0x0009)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0009
        0000180a-0000-1000-8000-00805f9b34fb
        Device Information
Characteristic (Handle 0x8724)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0009/char000a
        00002a25-0000-1000-8000-00805f9b34fb
        Serial Number String
Characteristic (Handle 0x8724)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0009/char000c
        00002a27-0000-1000-8000-00805f9b34fb
        Hardware Revision String
Characteristic (Handle 0x8724)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0009/char000e
        00002a28-0000-1000-8000-00805f9b34fb
        Software Revision String
Characteristic (Handle 0x8724)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0009/char0010
        00002a23-0000-1000-8000-00805f9b34fb
        System ID
Characteristic (Handle 0x8724)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0009/char0012
        00002a50-0000-1000-8000-00805f9b34fb
        PnP ID
Primary Service (Handle 0x0009)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0014
        00001530-0000-3512-2118-0009af100700
        Vendor specific
Characteristic (Handle 0x8cd4)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0014/char0015
        00001531-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0014/char0015/desc0017
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0xab38)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0014/char0018
        00001532-0000-3512-2118-0009af100700
        Vendor specific
Primary Service (Handle 0xc920)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service001a
        00001811-0000-1000-8000-00805f9b34fb
        Alert Notification Service
Characteristic (Handle 0xb8b4)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service001a/char001b
        00002a46-0000-1000-8000-00805f9b34fb
        New Alert
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service001a/char001b/desc001d
        00002901-0000-1000-8000-00805f9b34fb
        Characteristic User Description
Characteristic (Handle 0xd9a8)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service001a/char001e
        00002a44-0000-1000-8000-00805f9b34fb
        Alert Notification Control Point
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service001a/char001e/desc0020
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Primary Service (Handle 0xc920)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0021
        00001802-0000-1000-8000-00805f9b34fb
        Immediate Alert
Characteristic (Handle 0xeb34)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0021/char0022
        00002a06-0000-1000-8000-00805f9b34fb
        Alert Level
Primary Service (Handle 0xc920)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0024
        0000180d-0000-1000-8000-00805f9b34fb
        Heart Rate
Characteristic (Handle 0xfc04)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0024/char0025
        00002a37-0000-1000-8000-00805f9b34fb
        Heart Rate Measurement
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0024/char0025/desc0027
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0x10f8)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0024/char0028
        00002a39-0000-1000-8000-00805f9b34fb
        Heart Rate Control Point
Primary Service (Handle 0xc920)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a
        0000fee0-0000-1000-8000-00805f9b34fb
        Anhui Huami Information Technology Co.
Characteristic (Handle 0x1d74)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char002b
        00002a2b-0000-1000-8000-00805f9b34fb
        Current Time
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char002b/desc002d
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0x3838)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char002e
        00000001-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char002e/desc0030
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0x4b58)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0031
        00000002-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0031/desc0033
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0x6868)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0034
        00000003-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0034/desc0036
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0x8368)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0037
        00002a04-0000-1000-8000-00805f9b34fb
        Peripheral Preferred Connection Parameters
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0037/desc0039
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0x9498)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char003a
        00000004-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char003a/desc003c
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0xa538)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char003d
        00000005-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char003d/desc003f
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0xb4a8)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0040
        00000006-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0040/desc0042
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0xc428)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0043
        00000007-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0043/desc0045
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0xd3a8)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0046
        00000008-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0046/desc0048
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0xeae8)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0049
        00000010-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0049/desc004b
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0xf868)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char004c
        00000020-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char004c/desc004e
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0x1b28)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char004f
        0000000e-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char004f/desc0051
        00002901-0000-1000-8000-00805f9b34fb
        Characteristic User Description
Characteristic (Handle 0x2658)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0052
        0000000f-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0052/desc0054
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0x36f8)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0055
        00000011-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0055/desc0057
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0x45d8)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0058
        00000012-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0058/desc005a
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0x6488)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char005b
        00000013-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char005b/desc005d
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Primary Service (Handle 0xc920)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e
        0000fee1-0000-1000-8000-00805f9b34fb
        Anhui Huami Information Technology Co.
Characteristic (Handle 0x3974)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char005f
        00000009-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char005f/desc0061
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Characteristic (Handle 0x8f08)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char0062
        0000fedd-0000-1000-8000-00805f9b34fb
        Jawbone
Characteristic (Handle 0x8f08)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char0064
        0000fede-0000-1000-8000-00805f9b34fb
        Coin, Inc.
Characteristic (Handle 0x8f08)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char0066
        0000fedf-0000-1000-8000-00805f9b34fb
        Design SHIFT
Characteristic (Handle 0x8f08)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char0068
        0000fed0-0000-1000-8000-00805f9b34fb
        Apple, Inc.
Characteristic (Handle 0x8f08)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char006a
        0000fed1-0000-1000-8000-00805f9b34fb
        Apple, Inc.
Characteristic (Handle 0x8f08)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char006c
        0000fed2-0000-1000-8000-00805f9b34fb
        Apple, Inc.
Characteristic (Handle 0x8f08)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char006e
        0000fed3-0000-1000-8000-00805f9b34fb
        Apple, Inc.
Characteristic (Handle 0x8f08)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char0070
        0000fec1-0000-3512-2118-0009af100700
        Vendor specific
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char0070/desc0072
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
Primary Service (Handle 0xc920)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0073
        00003802-0000-1000-8000-00805f9b34fb
        Unknown
Characteristic (Handle 0x63b4)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0073/char0074
        00004a02-0000-1000-8000-00805f9b34fb
        Unknown
Descriptor (Handle 0x0015)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0073/char0074/desc0076
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
```

## miband4 UUIDs, services, characteristics, descriptors

The following is logged once successfully connected to the miband using `bluetoothctl`.

```sh
[CHG] Device D1:C5:15:51:03:89 Connected: yes
Connection successful
[NEW] Primary Service (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0008
        00001801-0000-1000-8000-00805f9b34fb
        Generic Attribute Profile
[NEW] Primary Service (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0009
        0000180a-0000-1000-8000-00805f9b34fb
        Device Information
[NEW] Characteristic (Handle 0xea8d)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0009/char000a
        00002a25-0000-1000-8000-00805f9b34fb
        Serial Number String
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0009/char000c
        00002a27-0000-1000-8000-00805f9b34fb
        Hardware Revision String
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0009/char000e
        00002a28-0000-1000-8000-00805f9b34fb
        Software Revision String
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0009/char0010
        00002a23-0000-1000-8000-00805f9b34fb
        System ID
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0009/char0012
        00002a50-0000-1000-8000-00805f9b34fb
        PnP ID
[NEW] Primary Service (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0014
        00001530-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0014/char0015
        00001531-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0x7554)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0014/char0015/desc0017
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0014/char0018
        00001532-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Primary Service (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service001a
        00001811-0000-1000-8000-00805f9b34fb
        Alert Notification Service
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service001a/char001b
        00002a46-0000-1000-8000-00805f9b34fb
        New Alert
[NEW] Descriptor (Handle 0xa8b4)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service001a/char001b/desc001d
        00002901-0000-1000-8000-00805f9b34fb
        Characteristic User Description
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service001a/char001e
        00002a44-0000-1000-8000-00805f9b34fb
        Alert Notification Control Point
[NEW] Descriptor (Handle 0x8b84)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service001a/char001e/desc0020
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Primary Service (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0021
        00001802-0000-1000-8000-00805f9b34fb
        Immediate Alert
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0021/char0022
        00002a06-0000-1000-8000-00805f9b34fb
        Alert Level
[NEW] Primary Service (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0024
        0000180d-0000-1000-8000-00805f9b34fb
        Heart Rate
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0024/char0025
        00002a37-0000-1000-8000-00805f9b34fb
        Heart Rate Measurement
[NEW] Descriptor (Handle 0xa084)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0024/char0025/desc0027
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0024/char0028
        00002a39-0000-1000-8000-00805f9b34fb
        Heart Rate Control Point
[NEW] Primary Service (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a
        0000fee0-0000-1000-8000-00805f9b34fb
        Anhui Huami Information Technology Co.
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char002b
        00002a2b-0000-1000-8000-00805f9b34fb
        Current Time
[NEW] Descriptor (Handle 0xac84)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char002b/desc002d
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char002e
        00000001-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0xb2e4)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char002e/desc0030
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0031
        00000002-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0xc174)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0031/desc0033
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0034
        00000003-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0xc504)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0034/desc0036
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0037
        00002a04-0000-1000-8000-00805f9b34fb
        Peripheral Preferred Connection Parameters
[NEW] Descriptor (Handle 0xcb64)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0037/desc0039
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char003a
        00000004-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0xd1c4)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char003a/desc003c
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char003d
        00000005-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0xd7e4)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char003d/desc003f
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0040
        00000006-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0xde14)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0040/desc0042
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0043
        00000007-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0xe444)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0043/desc0045
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0046
        00000008-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0xea74)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0046/desc0048
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0049
        00000010-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0x12f4)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0049/desc004b
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char004c
        00000020-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0x0d54)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char004c/desc004e
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char004f
        0000000e-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0x1334)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char004f/desc0051
        00002901-0000-1000-8000-00805f9b34fb
        Characteristic User Description
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0052
        0000000f-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0x1994)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0052/desc0054
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0055
        00000011-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0x1ff4)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0055/desc0057
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xea8d)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0058
        00000012-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0x3274)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char0058/desc005a
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char005b
        00000013-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0x38a4)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service002a/char005b/desc005d
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Primary Service (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e
        0000fee1-0000-1000-8000-00805f9b34fb
        Anhui Huami Information Technology Co.
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char005f
        00000009-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0x6384)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char005f/desc0061
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char0062
        0000fedd-0000-1000-8000-00805f9b34fb
        Jawbone
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char0064
        0000fede-0000-1000-8000-00805f9b34fb
        Coin, Inc.
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char0066
        0000fedf-0000-1000-8000-00805f9b34fb
        Design SHIFT
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char0068
        0000fed0-0000-1000-8000-00805f9b34fb
        Apple, Inc.
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char006a
        0000fed1-0000-1000-8000-00805f9b34fb
        Apple, Inc.
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char006c
        0000fed2-0000-1000-8000-00805f9b34fb
        Apple, Inc.
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char006e
        0000fed3-0000-1000-8000-00805f9b34fb
        Apple, Inc.
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char0070
        0000fec1-0000-3512-2118-0009af100700
        Vendor specific
[NEW] Descriptor (Handle 0x6324)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service005e/char0070/desc0072
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Primary Service (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0073
        00003802-0000-1000-8000-00805f9b34fb
        Unknown
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0073/char0074
        00004a02-0000-1000-8000-00805f9b34fb
        Unknown
[NEW] Descriptor (Handle 0x6c24)
        /org/bluez/hci0/dev_D1_C5_15_51_03_89/service0073/char0074/desc0076
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[CHG] Device D1:C5:15:51:03:89 UUIDs: 00001530-0000-3512-2118-0009af100700
[CHG] Device D1:C5:15:51:03:89 UUIDs: 00001800-0000-1000-8000-00805f9b34fb
[CHG] Device D1:C5:15:51:03:89 UUIDs: 00001801-0000-1000-8000-00805f9b34fb
[CHG] Device D1:C5:15:51:03:89 UUIDs: 00001802-0000-1000-8000-00805f9b34fb
[CHG] Device D1:C5:15:51:03:89 UUIDs: 0000180a-0000-1000-8000-00805f9b34fb
[CHG] Device D1:C5:15:51:03:89 UUIDs: 0000180d-0000-1000-8000-00805f9b34fb
[CHG] Device D1:C5:15:51:03:89 UUIDs: 00001811-0000-1000-8000-00805f9b34fb
[CHG] Device D1:C5:15:51:03:89 UUIDs: 00003802-0000-1000-8000-00805f9b34fb
[CHG] Device D1:C5:15:51:03:89 UUIDs: 0000fee0-0000-1000-8000-00805f9b34fb
[CHG] Device D1:C5:15:51:03:89 UUIDs: 0000fee1-0000-1000-8000-00805f9b34fb
[CHG] Device D1:C5:15:51:03:89 ServicesResolved: yes
[CHG] Device D1:C5:15:51:03:89 Modalias: bluetooth:v0157p0024d0101
```
