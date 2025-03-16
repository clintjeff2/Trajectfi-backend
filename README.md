# TRAJECTFI

## INTRODUCTION
Trajectfi is a peer-to-peer NFT collateralization and lending platform built on the starknet ecosystem. It enables peer-to-peer NFT collateralization and token borrowing. Trajectfi deal with specifically accepted NFTs to be collateralized and specifically accepted token to be borrowed.

For borrowers, Trajectfi provides a protocol to get token loans with owned assets. All loans have fixed terms without price-based liquidation, and borrowers can renegotiate existing loans.

For lenders, Trajectfi provides a platform for generating attractive yields  (interest) on owned tokens and also offering the chance to acquire NFTs at discounts to market price if a borrower defaults.

The Loan lifecycle:
- Borrowers list collateral: This collateral will be their NFT that is accepted for collateral in Trajectfi. The borrower can list their collateral for loan and optionally their borrow terms i.e (the amount to borrow, the deadline to pay back (in days), the token to borrow, the APY (the yield to be receive after borrow payment) )
- Lenders view listed collaterals and make loan offer, a counter loan offer or accept borrower listed offer
- Borrowers accept lender's offer and the due diligence is done (transferring NFT to escrow and transferring token to borrower from lender)
- Borrowers either pay before the due date of the loan or the NFT is given to the lender after the due date.

Note: Loan can be renegotiated after being taken. All last acceptance is done by the borrower whether it is accepting lender acceptance of offer or accepting lender own offer for either loan negotiation or original loan listing.

## Schema structure and function
