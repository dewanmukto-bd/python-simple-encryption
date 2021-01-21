# This module contains functions that encrypt and decrypt messages using a Linear Feedback Shift Register (LFSR)
# @author dmimukto 2021

# Required modules are imported
from pcryt_bindec import *

# The standard possible Base64 characters are stored as a string for index referencing
BASE64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

# This function converts a character into a list of six 1's and 0's using Base64 encoding
def charToBin(c):
    binaryList = []
    # the standard set of Base64 characters are iterated over to find a match with the character being converted
    for index in range(len(BASE64)):
        # if a match is found...
        if c == BASE64[index]:
            # the fact here is that the decimal values correspond directly to the Base64 characters, so the decimal to binary conversion is more efficient
            # the "decToBin" function is called from the "bindec.py" module
            # the resulting list of binary values is aliased to the output list
            binaryList.extend(decToBin(index))
    return binaryList

# This function converts a list of six 1's and 0's into a character using Base64 encoding
def binToChar(b):
    # the binary value is converted to a decimal value
    decValue = binToDec(b)
    # the decimal value is converted to a character value relying on the fact that Base64 characters have their index positions corresponding to decimals
    charValue = BASE64[decValue]
    # mission is accomplished for this function, so it returns the character as output
    return charValue

# This function converts a string of characters into a list of 1's and 0's using Base64 encoding
def strToBin(s):
    # an empty list is created to capture the output
    binaryList = []
    # the whole string is iterated over
    for index in range(len(s)):
        # every individual character is converted to binary
        binaryList.extend(charToBin(s[index]))
    # the final output is a list of binary values
    return binaryList

# This function converts a list of 1's and 0's into a string of characters using Base64 encoding
def binToStr(b_list):
    # an empty string is created to store the final result
    outputString = ""
    # the list of binary values is iterated over, skipping 6 values at a time
    for index in range(0,len(b_list),6):
        # for convenience, the list is split at 6-value intervals
        sixBitChunk = b_list[index:index+6]
        # at every iteration of this loop, the resultant character is stored into the output string
        outputString += binToChar(sixBitChunk)
    # when the whole list has been converted back to strings, the function returns it
    return outputString

# This function returns a pseudo-random list of 1s and 0s, generated by an [N,k] LFSR, where N = length of seed
def generatePad(seed, k, l):
    # the N in the [N,k] LFSR is defined
    N = len(seed)
    # an empty list is created for collecting the output string
    padOutput = []
    # the linear scan
    for index in range(l):
        # the feedback
        if seed[N-1]==seed[k]:
            padOutput.append(0)
        else:
            padOutput.append(1)
        # the shift
        seed = seed[1:]
        # the register
        seed.append(padOutput[-1])
    # the final output of a list of binary values
    return padOutput

# This function takes a string message and returns it as an encrypted string using an [N,k] LFSR
def encrypt(message, seed, k):
    # converts message string to binary
    messageBinary = strToBin(message)
    # generates the pseudo-random pad using [N,k] LFSR
    pseudoRandomPad = generatePad(seed, k, len(messageBinary))
    # generates the encrypted ciphertext in binary form by XORing
    cipherBinary = xorify(pseudoRandomPad, messageBinary)
    # converts the ciphertext to string form
    cipherString = binToStr(cipherBinary)
    # the encrypted message is output
    return cipherString

# This is an extra function for simulating a XOR mechanism over 2 lists of equal length
def xorify(inputList1, inputList2):
    # an empty list is created to store the output
    outputList = []
    # the two input lists are iterated over
    for index in range(len(inputList1)):
        # as in typical XOR logic, if the two values are same, the result is 0
        if inputList1[index]==inputList2[index]:
            outputList.append(0)
        # if not same, then result is 1
        else:
            outputList.append(1)
    return outputList




