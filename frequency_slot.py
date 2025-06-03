"""
Copyright 2025 Pete Stephenson

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
"""

import math
import argparse

# REFERENCE1 https://github.com/meshtastic/firmware/blob/f6ed10f3298abf6896892ca7906d3231c8b3f567/src/mesh/RadioInterface.cpp
# REFERENCE2 https://github.com/meshtastic/meshtastic/blob/2ec6cb1ebd819baaf64ea9b00c7bde0b59d24160/docs/about/overview/radio-settings.mdx - table in the "Presets" section.

# Frequency range and other parameters (US)
# See REFERENCE1 L15 and L26, REFERENCE2.
freq_start = 902.0      # MHz
freq_end = 928.0        # MHz
spacing = 0
bw = 250                # default, unless altered by some preset names

def get_bandwidth_khz(channel_name):
    """Determine the bandwidth in kHz based on channel name."""
    if channel_name == "ShortTurbo":
        return 500
    elif channel_name in ["LongModerate", "LongSlow"]:
        return 125
    else:
        return 250  # Default bandwidth
    
def calculate_num_freq_slots(freq_start, freq_end, spacing, bw):
    """Calculate the total number of frequency slots."""
    return math.floor((freq_end - freq_start) / (spacing + (bw / 1000)))
    
# Hash function: djb2 by Dan Bernstein
# See REFERENCE1 @ L395.
def hash_string(s):
    hash_value = 5381
    mask = 0xFFFFFFFF # 32-bit mask to emulate uint32_t behavior
    for c in s:
        hash_value = (((hash_value << 5) + hash_value) + ord(c))  # hash * 33 + c
        hash_value &= mask # Mask to 32 bits.
    return hash_value

def determine_frequency_slot(channel_name, num_freq_slots):
    """Determine the frequency slot from the channel name."""
    return hash_string(channel_name) % num_freq_slots

def calculate_frequency(freq_start, frequency_slot, bw):
    """Calculate the frequency using the new formula."""
    return freq_start + (bw / 2000) + (frequency_slot * (bw / 1000))

def print_results(channel_name, num_freq_slots, frequency_slot, freq):
    """Print results"""
    print(f"Channel Name: {channel_name}")
    print(f"Number of Frequency Slots: {num_freq_slots}")
    # See REFERENCE1 @ L552 and L584
    # frequency_slot is actually (frequency_slot - 1), since modulus (%) returns values from 0 to (numFrequencySlots - 1)
    print(f"Frequency Slot: {frequency_slot + 1}") 
    print(f"Selected Frequency: {freq} MHz")

def main():
    # Argument parser setup.
    parser = argparse.ArgumentParser(description="Override channel name for channel frequency calculation.")
    parser.add_argument("--channel-name", "-n", type=str, default="LongFast",
                    help="Specify the channel name (default: 'LongFast').")
    args = parser.parse_args()
    
    # Get the channel name from arguments.
    channel_name = args.channel_name
    bw = get_bandwidth_khz(channel_name)

    # Calculate the number of LoRa channels in the region.
    num_freq_slots = calculate_num_freq_slots(freq_start, freq_end, spacing, bw)

    # Determine the frequency slot.
    frequency_slot = determine_frequency_slot(channel_name, num_freq_slots)

    # Calculate the frequency.
    freq = calculate_frequency(freq_start, frequency_slot, bw)
    
    # Print results
    print_results(channel_name, num_freq_slots, frequency_slot, freq)

# Entry point
if __name__ == "__main__":
    main()
