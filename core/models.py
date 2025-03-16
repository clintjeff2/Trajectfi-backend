import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# ENUMS


class LoanStatus(models.IntegerChoices):
    PENDING = 1, "Pending"
    EXPIRED = 2, "Expired"
    FORECLOSED = 3, "Foreclosed"
    REPAID = 4, "Repaid"


class LoanRenegotiationStatus(models.IntegerChoices):
    PENDING = 1, "Pending"
    COUNTERED = 2, "Countered"
    ACCEPTED = 3, "Accepted"


# MANAGERS


class BaseManager(UserManager):
    use_in_migrations = True

    def _create_user(self, public_key, **extra_fields):
        """
        Create and save a user with the given public key.
        """

        user = self.model(public_key=public_key, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, public_key, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(public_key, **extra_fields)

    def create_superuser(self, public_key, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        user = self.model(public_key=public_key, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


# MODELS


class BaseModel(models.Model):
    """
    ### Description
    The superclass model for every model defined in this file.
    This ensures that every model (table) has a:
    - A UUID id field,
    - A created_at field (this shows the date and time an entry was created)
    - An updated_at field (this shows the date and time an entry was updated)

    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("created_at",)

    @property
    def id_as_str(self) -> str:
        return str(self.id)


class User(AbstractUser, BaseModel):
    """
    ### Description
    This model represent a user in the application.
    The username, first_name and last_name fields are set to None
    because we are using Django's default AbstractUser model but
    we do not need the username, first_name and last_name fields.

    ### Fields:
    - email(str) - the email address of the user
    - public_key(str) - the wallet address of the user.

    All the fields should be unique.
    No two or more Users should have the same public_key or email address.
    """

    username = None
    first_name = None
    last_name = None
    email = models.EmailField(
        _("Email"),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    public_key = models.CharField(
        _("Public Key"),
        max_length=70,
        unique=True,
    )
    objects = BaseManager()

    USERNAME_FIELD = "public_key"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.public_key


class AcceptedNFT(BaseModel):
    """
    ### Description
    This model represent NFTs that are accepted in this application.
    Only the accepted NFTs can be used to take out a loan.
    This model will mostly be use for filtering listings based on a collection

    ### Fields:
    - name(str) - the name of the NFT collection
    - contract_address(str) - the contract address of the NFT collection.

    """

    name = models.CharField(
        _("Collection Name"),
        max_length=70,
        unique=True,
    )
    contract_address = models.CharField(
        _("Collection Contract Address"),
        max_length=70,
        unique=True,
    )

    def __str__(self) -> str:
        return self.name


class AcceptedToken(BaseModel):
    """
    ### Description
    This model represent Fungible Tokens that are accepted in this application.
    Only the accepted token can be used to give a loan.


    ### Fields:
    - name(str) - the name of the fungible token.
    - contract_address(str) - the contract address of the fungible token.
    - token_decimal(int) -  the decimal of the token

    """

    name = models.CharField(
        _("Token Name"),
        max_length=70,
        unique=True,
    )
    contract_address = models.CharField(
        _("Token Contract Address"),
        max_length=70,
        unique=True,
    )
    token_decimal = models.IntegerField(_("Token Decimal"))

    def __str__(self) -> str:
        return self.name


class Listing(BaseModel):
    """
    ### Description
    This model represent an NFT collateral listing to take out a loan.
    Borrowers list their NFTs and wait for loan offers.
    Optionally, borrowers can add the
    token_contract_address, borrow_amount, repayment_amount and
    duration to the listing.


    ### Fields:
    - user(foreignkey) - the reference to the borrower via the user model.
    - nft_contract_address(str) - the contract address of the collateral NFT.
    - nft_token_id(int) - the token id of the NFT
    - token_contract_address(str) - the contract address of the token (optional)
    - borrow_amount(int) - the amount of token to
    borrow (in the token decimal) (optional)
    - repayment_amount(int) - the amount of token to be
    repaid (in the token decimal) (optional)
    - duration (int) - the duration in seconds of when the loan must be repaid
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nft_contract_address = models.CharField(_("NFT Contract Address"), max_length=70)
    nft_token_id = models.PositiveBigIntegerField(_("NFT Token ID"))
    token_contract_address = models.CharField(
        _("Token Contract Address"), max_length=70, null=True, blank=True
    )
    borrow_amount = models.PositiveBigIntegerField(
        _("Borrow Amount"), null=True, blank=True
    )
    repayment_amount = models.PositiveBigIntegerField(
        _("Repayment Amount"), null=True, blank=True
    )
    duration = models.PositiveIntegerField(_("Loan Duration"), null=True, blank=True)

    def __str__(self) -> str:
        return f"Token: {self.token_contract_address}, NFT: {self.nft_contract_address}"


class Offer(BaseModel):
    """
    ### Description
    This model represent a loan offer by a lender.


    ### Fields:
    - user(foreignkey) - the reference to the lender via the user model.
    - listing(foreignkey) - the reference to the collateral listing via the
    listing model.
    - borrow_amount(int) - the amount of token to
    lend (in the token decimal) (optional)
    - repayment_amount(int) - the amount of token to be
    repaid (in the token decimal) (optional)
    - duration (int) - the duration in seconds of when the loan must be repaid
    - signature (str) - the crypto signature of the offer signed by the lender
    - signature_expiry (int) - the timestamp of when the signature expires
    - signature_chain_id (int) - the chain id of the signature
    - signature_unique_id (int) -  the unique id used for the signature
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    token_contract_address = models.CharField(
        _("Token Contract Address"),
        max_length=70,
    )
    borrow_amount = models.PositiveBigIntegerField(
        _("Borrow Amount"), null=True, blank=True
    )
    repayment_amount = models.PositiveBigIntegerField(
        _("Repayment Amount"), null=True, blank=True
    )
    duration = models.PositiveIntegerField(_("Loan Duration"))
    signature = models.TextField(_("Signature"))
    signature_expiry = models.PositiveIntegerField(_("Signature Expiry"))
    signature_chain_id = models.IntegerField(_("Signature Chain Id"))
    signature_unique_id = models.PositiveBigIntegerField(_("Signature Unique Id"))

    def __str__(self) -> str:
        return f"Listing #{self.listing.id_as_str}, Lend amount: {self.borrow_amount}"


class Loan(BaseModel):
    """
    ### Description
    This model represent a loan.

    ### Fields:
    - borrower(str) - the contract address of the borrower.
    - lender(str) - the contract address of the lender.
    - loan_id (int) - the id of the loan on the smart contract.
    - nft_contract_address(str) - the contract address of the collateral NFT.
    - nft_token_id(int) - the token id of the NFT
    - token_contract_address(str) - the contract address of the token
    - borrow_amount(int) - the amount of token to lend (in the token decimal)
    - repayment_amount(int) - the amount of token to be
    repaid (in the token decimal)
    - duration (int) - the duration in seconds of when the loan must be repaid
    - start_time(datetime) - the date the loan started
    """

    borrower = models.CharField(_("Borrower"), max_length=70)
    lender = models.CharField(_("Lender"), max_length=70)
    loan_id = models.PositiveBigIntegerField(_("Loan Id"))
    nft_contract_address = models.CharField(_("NFT Contract Address"), max_length=70)
    nft_token_id = models.PositiveBigIntegerField(_("NFT Token ID"))
    token_contract_address = models.CharField(
        _("Token Contract Address"),
        max_length=70,
    )
    borrow_amount = models.PositiveBigIntegerField(_("Borrow Amount"))
    repayment_amount = models.PositiveBigIntegerField(_("Repayment Amount"))
    duration = models.PositiveIntegerField(_("Loan Duration"))
    start_time = models.DateTimeField(_("Loan Start Time"))
    status = models.IntegerField(
        _("Loan Status"), choices=LoanStatus.choices, default=LoanStatus.PENDING
    )

    def __str__(self) -> str:
        return str(self.loan_id)


class RenegotiationOffer(BaseModel):
    """
    ### Description
    This model represent a renegotiation offer of a loan.
    This renegotiation offer can be raised by either the lender or the borrower.
    When the lender raises the renegotiation offer, all optional field are filled,
    When the borrower raises the renegotiation offer, all optional field are blank.

    ### Fields:
    - loan(foreignkey) - the reference to the loan via the loan model.
    - user(foreignkey) - the reference to the lender or borrower that raised the
    renegotiation offer via the user model.
    - repayment_amount(int) - the amount of token to be repaid (in the token decimal)
    - duration (int) - the duration in seconds of when the loan must be repaid
    - incentive (int) - an optional commission to be given to the lender for accepting
    the offer (default to 0)
    - signature (str) - the crypto signature of the offer signed by the
    lender (optional)
    - signature_expiry (int) - the timestamp of when the signature expires (optional)
    - signature_chain_id (int) - the chain id of the signature (optional)
    - signature_unique_id (int) -  the unique id used for the signature (optional)
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    repayment_amount = models.PositiveBigIntegerField(_("Repayment Amount"))
    duration = models.PositiveIntegerField(_("Loan Duration"))
    incentive = models.PositiveBigIntegerField(_("Incentive"))
    signature = models.TextField(_("Signature"), blank=True, null=True)
    signature_expiry = models.PositiveIntegerField(
        _("Signature Expiry"), null=True, blank=True
    )
    signature_chain_id = models.IntegerField(
        _("Signature Chain Id"), null=True, blank=True
    )
    signature_unique_id = models.PositiveBigIntegerField(
        _("Signature Unique Id"), null=True, blank=True
    )
    status = models.IntegerField(
        _("Status"),
        choices=LoanRenegotiationStatus.choices,
        default=LoanRenegotiationStatus.PENDING,
    )

    def __str__(self):
        return f"Loan #{self.loan.loan_id}, status: {self.status.get_status_display()}"
