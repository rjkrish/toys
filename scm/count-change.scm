;
; Count the number of ways to make change for a given
; amount using 3 kinds of coins
;

(define (count-change amount)
    (cc amount 3 0)
)

(define (cc amount kinds-of-coins depth)
    (display-call amount kinds-of-coins depth ) (display " => ") 
    (cond   ((= amount 0) 
               (begin (display "1") (newline) 1))
            ((or (< amount 0) (= kinds-of-coins 0)) 
               (begin (display "0") (newline) 0))
            (else 
               (begin
                    (display-call amount (- kinds-of-coins 1) 0) 
                    (display " + " ) 
                    (display-call 
                        (- amount (first-denomination kinds-of-coins)) 
                        kinds-of-coins 0 ) 
                    (newline) 
               )
               (+ (cc amount (- kinds-of-coins 1) (+ depth 1))
                  (cc (- amount (first-denomination kinds-of-coins))
                       kinds-of-coins (+ depth 1) ))
            )
    )
)

(define (first-denomination kinds-of-coins)
    (cond   ((= kinds-of-coins 1) 1)
            ((= kinds-of-coins 2) 2)
            ((= kinds-of-coins 3) 5)
            ((= kinds-of-coins 4) 10)
    )
)

(define (display-call a k i) 
    (display-indent i)
    (display "[A=" ) (display a ) 
    (display ", K=" ) (display k ) (display "]") 
)

(define (display-indent depth)
    (cond ( (< depth 1) (begin  0)) 
          ( else        (begin  (display "   ")
                                (display-indent (- depth 1))))
    )
)
