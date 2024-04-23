-- CreateTable
CREATE TABLE "hb_user_data" (
    "data_id" TEXT NOT NULL,
    "data_source" VARCHAR(450) NOT NULL,
    "data_chunks" TEXT[],
    "user_id" INTEGER NOT NULL,

    CONSTRAINT "hb_user_data_pkey" PRIMARY KEY ("data_id")
);

-- AddForeignKey
ALTER TABLE "hb_user_data" ADD CONSTRAINT "hb_user_data_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "hb_users"("user_id") ON DELETE RESTRICT ON UPDATE CASCADE;
