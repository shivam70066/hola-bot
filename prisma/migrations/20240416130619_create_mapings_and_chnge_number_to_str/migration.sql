/*
  Warnings:

  - You are about to drop the column `user_created_at` on the `hb_users` table. All the data in the column will be lost.
  - You are about to drop the column `user_deleted_at` on the `hb_users` table. All the data in the column will be lost.
  - You are about to drop the column `user_updated_at` on the `hb_users` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "hb_users" DROP COLUMN "user_created_at",
DROP COLUMN "user_deleted_at",
DROP COLUMN "user_updated_at",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "deleted_at" TIMESTAMP(3),
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ALTER COLUMN "user_number" SET DATA TYPE TEXT;
