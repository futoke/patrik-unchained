from enum import Enum
from typing import Annotated, Optional

from fastapi import Query
from pydantic import BaseModel, Field


class Eyes(str, Enum):
    left_eye = "left_eye"
    right_eye = "right_eye"


class Easing(str, Enum):
    linear      = "linear"
    ease_in     = "ease_in"
    ease_out    = "ease_out"
    ease_in_out = "ease_in_out"


class EasingRus(str, Enum):
    linear      = "линейно"
    ease_in     = "плавно_вначале"
    ease_out    = "плавно_вконце"
    ease_in_out = "плавно"


class Animations(str, Enum):
    wink              = "wink"
    widen             = "widen"
    eye_roll          = "eye_roll"
    tear_drop         = "tear_drop"
    blinking          = "blinking"
    fluctuating       = "fluctuating"
    fluctuating_upper = "fluctuating_upper"
    twitching_lower   = "twitching_lower"
    snoozing          = "snoozing"


class ExpressionsRus(str, Enum):
    annoyed            = "раздраженный"
    anxious            = "тревожный"     
    apologetic         = "извиняющийся"           
    awkward            = "неуклюжий"         
    blinking           = "мигающий"          
    bored              = "скучающий"          
    crying             = "плачущий" 
    default            = "обычный"    
    determined         = "определенный"    
    embarrased         = "смущенный"          
    evil               = "злой"                    
    excited            = "взволнованный"                       
    exhausted          = "измученный"              
    flustered          = "взволнованный"                 
    furious            = "яростный"                   
    giggle             = "хихикающий"                                                                             
    happy              = "счастливый"             
    in_love            = "влюбленный"                
    mischievous        = "озорной"                        
    realized_something = "понял что-то"                   
    sad                = "грустный"                  
    sassy              = "дерзкий"                     
    scared             = "испуганный"                   
    shocked            = "шокирован"                     
    snoozing           = "дремлющий"                                                              
    starstruck         = "звездный"                   
    stuck_up           = "застрявший"                    
    thinking           = "думающий"                     
    tired              = "усталый",                        
    upset              = "расстроенный"                       
    winking            = "подмигивающий"                        
    wow                = "ух-ты"


class Expressions(str, Enum):
    annoyed            = "annoyed"          
    anxious            = "anxious"           
    apologetic         = "apologetic"        
    awkward            = "awkward"           
    blinking           = "blinking"          
    bored              = "bored"             
    crying             = "crying"            
    default            = "default"           
    determined         = "determined"        
    embarrased         = "embarrased"        
    evil               = "evil"              
    excited            = "excited"           
    exhausted          = "exhausted"         
    flustered          = "flustered"         
    furious            = "furious"           
    giggle             = "giggle"            
    happy              = "happy"             
    in_love            = "in-love"           
    mischievous        = "mischievous"       
    realized_something = "realized-something"
    sad                = "sad"               
    sassy              = "sassy"             
    scared             = "scared"            
    shocked            = "shocked"           
    snoozing           = "snoozing"          
    starstruck         = "starstruck"        
    stuck_up           = "stuck-up"          
    thinking           = "thinking"          
    tired              = "tired"             
    upset              = "upset"             
    winking            = "winking"           
    wow                = "wow"               


class Gaze(BaseModel):
    easing: Easing = Easing.linear
    speed: float = 50.0
    direction: list[Annotated[float, Query(ge=0, le=1)]] = [0.5, 0.5]


class Animation(BaseModel):
    animation: Animations | None = None
    average_delay: Annotated[int | None, Query(ge=0)] = None
    duration: Annotated[int | None, Query(ge=0)] = None
    easing: Easing | None = None
    elements: list[Eyes | None] = [Eyes.left_eye, Eyes.right_eye]
    random: bool | None = None
    left: Annotated[int | None, Query(ge=0)] = None
    top: Annotated[int | None, Query(ge=0)] = None
    width: Annotated[int | None, Query(ge=0)] = None
    height: Annotated[int | None, Query(ge=0)] = None
    scaleX: Annotated[float | None, Query(ge=0)] = None
    scaleY: Annotated[float | None, Query(ge=0)] = None
    radius: Annotated[float | None, Query(ge=0)] = None
    angle: Annotated[int | None, Query(ge=0, le=360)] = None
    skewX: Annotated[int | None, Query(ge=0, le=360)] = None


class Face(BaseModel):
    expression: Expressions
    # expression_rus: ExpressionsRus | None = None
    gaze: Gaze | None = None
    animation: Animation | None = None
               