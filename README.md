# meshtastic_frequency_slot_calculator
Calculates the frequency slot for a given Meshtastic channel name.

## Motivation

In the US region, Meshtastic uses the `LONG_FAST` [modem preset](https://meshtastic.org/docs/configuration/radio/lora/#modem-preset) by default. This works well in many areas, but I live in the San Francisco Bay Area which has many nodes and thus the [local group BayMe.sh](https://bayme.sh/) has recommended that users use the `MEDIUM_SLOW` preset instead to minimize network congestion.

[BayMe.sh provides instructions to set up one's node to use that configuration](https://bayme.sh/docs/getting-started/recommended-settings/) on the primary channel. If one keeps the [frequency slot](https://meshtastic.org/docs/configuration/radio/lora/#frequency-slot) set to the default value of `0`, Meshtastic will use a hash-based algorithm for determining the frequency slot corresponding to that channel name. However, it can be desirable to [use a private primary channel and the default as a secondary channel](https://meshtastic.org/docs/configuration/tips/#creating-a-private-primary-with-default-secondary). 

Unfortunately, there's a complication: Meshtastic uses the hash-based algorithm based only on the name of the [*primary channel*](https://meshtastic.org/docs/configuration/radio/channels/). That is, both the primary and any secondary channels share the same frequency slot as the primary channel.

When a node is configured to use the default `LONG_FAST` modem preset, the default primary channel name is `LongFast`[^1]  In the US, the `LongFast` channel uses frequency slot 20 (906.875 MHz). If one uses a private primary channel with a different name and moves the default `LongFast` channel to a secondary channel, they need to explicitly set the frequency slot for the primary channel to `20` (for `LongFast`) in order to see the default traffic on the secondary channel.

I was interested in setting up a private primary channel and moving the defaults to a secondary channel, but I did not know the frequency slot for the `MediumSlow` channel (the name of the default channel for the `MEDIUM_SLOW` modem preset). Using `20` wouldn't work, since that's the slot for `LongFast`, not `MediumSlow`. In order to get the local `MediumSlow` traffic and participate in the mesh, I needed to know the frequency slot for the `MediumSlow` channel.

Fortunately, Meshtastic is open source and I was able to [read the source](https://github.com/meshtastic/firmware/blob/f6ed10f3298abf6896892ca7906d3231c8b3f567/src/mesh/RadioInterface.cpp) and implement the frequency slot calculation algorithm in python so I could calculate the slot for the `MediumSlow` channel.

## Usage
```
python3 frequency_slot.py

Channel Name: LongFast
Number of Frequency Slots: 104
Frequency Slot: 20
Selected Frequency: 906.875 MHz
```

```
python3 frequency_slot.py -n MediumSlow

Channel Name: MediumSlow
Number of Frequency Slots: 104
Frequency Slot: 52
Selected Frequency: 914.875 MHz
```

## Limitations
- Currently only produces output for the US region. I hope to add additional regions in the future.

### Footnotes
[^1]: Although similarly named, the modem preset and channel name are different things entirely: the modem preset defines the bandwidth, spreading factor, and other parameters for the LoRa mdoem itself, while the channel name being essentially a chat room name.