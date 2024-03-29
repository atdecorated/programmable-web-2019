from spending_tracker.cli import db
from spending_tracker.db_models.db_models import WalletModel, UserModel
from spending_tracker.utils.money_handler import money_add, money_subtract
from spending_tracker.resources.errormodels import create_error_response


class Wallet:
    def __init__(self, user):
        self.user = user

    def add_money(self, money: float, subtract=False) -> int:
        """Add money to db wallet
        Returns:
             int: 201 if successful
        """
        db_user = UserModel.query.filter_by(user=self.user).first()
        if db_user is None:
            create_error_response(404, title='Not found', message=f'User {self.user} was not found')
        if db_user.wallets:
            if not subtract:
                db_user.wallets[0].money = money_add(
                    db_user.wallets[0].money,
                    money
                )
            else:
                db_user.wallets[0].money = money_subtract(
                    -db_user.wallets[0].money,
                    money
                )
        else:
            wallet_model = WalletModel(
                user_id=db_user.id,
                money=money
            )
            db.session.add(wallet_model)
        db.session.commit()
        return 201

    def balance(self) -> dict:
        """Query wallet balance from db

        Returns:
            dict: If process is successful
            else return abort to API
        """
        user_name = UserModel.query.filter_by(user=self.user).first()
        if user_name is None:
            create_error_response(404, title='Not found', message=f'User {user_name} was not found')
        user_wallet = user_name.wallets[0]
        resp = dict(
            user=user_name.user,
            wallet=user_wallet.money
        )
        return resp
