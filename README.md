# meshtastic_frequency_slot_calculator
 Calculates the frequency slot for a given Meshtastic channel name.
 
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