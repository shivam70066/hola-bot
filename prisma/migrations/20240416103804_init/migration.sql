-- CreateTable
CREATE TABLE "hb_users" (
    "user_id" SERIAL NOT NULL,
    "user_name" VARCHAR(255) NOT NULL,
    "user_email" VARCHAR(255) NOT NULL,
    "user_password" TEXT NOT NULL,
    "user_number" INTEGER NOT NULL,

    CONSTRAINT "hb_users_pkey" PRIMARY KEY ("user_id")
);

-- CreateIndex
CREATE UNIQUE INDEX "hb_users_user_email_key" ON "hb_users"("user_email");
