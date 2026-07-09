# def main():
#     print("Hello from mcp!")


# if __name__ == "__main__":
#     main()

import random 
from fastmcp import FastMCP

mcp = FastMCP(name="Demo Server")

@mcp.tool 
def rool_dice(n_dice:int=1)-> list[int]:
    """Rolls a n_dice 6 sided dice and return result"""
    return [random.randint(1,6) for _ in range(n_dice)]

@mcp.tool
def add_number(a:float,b:float) -> float:
    """Add two numbers """
    return a+b

if __name__ == "__main__":
    mcp.run()