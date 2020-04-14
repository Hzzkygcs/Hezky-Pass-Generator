from hashlib import sha256 as sha

specialChar = "!#?$&%_~|"  #Should be static
caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  #Should be static
low  = caps.lower()  #Should be static
number = "0123456789"  #Should be static
allInOne = low+caps+specialChar+number  #Should be static
LENGTH = 14  #Should be static

def getSha(text, ENCODING = "utf-8"):
    if (type(text) != type(b'')):
        text = str(text).encode(ENCODING)
    return sha(text).hexdigest()

def XORbitwise(a, b):
    return chr( ord(a) ^ ord(b) )

def operation(str1, str2, operation = XORbitwise):
    newStr = ""
    for i in range( len( min(str1,str2) ) ):
        newStr += operation(str1[i], str2[i])
    return newStr

def process(text, ENCODING = "utf-8"):
    sha = list(getSha(text, ENCODING))
    firstLetter = ord(sha.pop(0)) + ord(sha.pop(0)) + ord(sha.pop(0)) + ord(sha.pop(0))
    secondLetter = int(sha.pop(0), 16)
    thirdLetter  = int(sha.pop(0), 16)
    sha2 = getSha(firstLetter, ENCODING)[:(3 + secondLetter * thirdLetter) % len(getSha(''))] 

    tmp = len(sha)//2
    part1 = getSha( sha[:tmp], ENCODING )
    part2 = getSha( sha[tmp:], ENCODING )
    part3 = operation(part1, part2)

    tmp = len(part3)//2
    part1 = getSha( part3[:tmp], ENCODING )
    part2 = getSha( part3[tmp:], ENCODING )
    part3 = list(part1 + part2)

    Sum = 0
    part4 = ""
    for i in range(len(part3)):
        Sum += ord(part3.pop(0))
        if (i%2 == 1):
            if (i%3 == 0):
                part4 += chr(Sum//2)
            elif (i%3 == 1):
                part4 += chr(Sum%256)
            elif (i%3 == 2):
                part4 += chr(  ((Sum*Sum)//2)%256  )

    part4 = list(part4)
    part5 = ""
    for i in range(len(part4)):
        part5 += chr( (
                        ord(part4.pop()) + int(sha2[i%len(sha2)],16)
                       ) % 256)
    return part5

def characterize(a, b):
    return allInOne[ (ord(a)^ord(b)) % len(allInOne) ]

def getPass(keyword, siteName, ENCODING = "utf-8"):
    site = siteName.lower()
    process1 = process(keyword, ENCODING)
    process2 = process(site, ENCODING)
    result   = list(operation(process1, process2, characterize))
    SpecialChar, Caps, Low, Number = (  specialChar[ ord(result.pop(-1)) % len(specialChar)],
                                        caps[ord(result.pop(0)) % len(caps)],
                                        low[ord(result.pop(-1)) % len(low)],
                                        number[ord(result.pop(0)) % len(number)]  )

    isAvailable = list(range(LENGTH)) # To make tmp1, tmp2, tmp3, and tmp4 unique each other
    tmp1 = isAvailable.pop( ord(result.pop(0)) % len(isAvailable)  )
    tmp2 = isAvailable.pop( ord(result.pop(-1)) % len(isAvailable)  )
    tmp3 = isAvailable.pop( ord(result.pop(0)) % len(isAvailable)  )
    tmp4 = isAvailable.pop( ord(result.pop(-1)) % len(isAvailable)  )
    

    # Following 4 lines -> to guarantee that the password consists of all of 
    # the required elements: Lower case, Upper case, number, and symbols.
    result[tmp1] = SpecialChar
    result[tmp2] = Caps
    result[tmp3] = Low
    result[tmp4] = Number

    result = ''.join(result)

    return result[:LENGTH]
    
